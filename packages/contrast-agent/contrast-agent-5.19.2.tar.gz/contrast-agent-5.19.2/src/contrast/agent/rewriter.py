# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib.abc
import importlib.machinery
import importlib.util
import types
import sys
import ast
import copy


import contrast
from contrast.agent import scope
from contrast.agent.assess.utils import clear_properties, track_and_tag
from contrast.agent.request_context import RequestContext
from contrast.agent.settings import Settings
from contrast.patches.rewriter import contrast__add, populate_rewritten_functions
from contrast.utils.decorators import fail_loudly
from contrast.utils.environ import test_environ
from contrast.extern import structlog as logging
from contrast.extern.wrapt.importer import _ImportHookChainedLoader

logger = logging.getLogger("contrast")


def _load_module(source, module: types.ModuleType, filename):
    """
    Convenience method to compile and execute the given module source

    It seems like we do not need any exception handling here since any
    exception that occurs gets handled further up by the import machinery and
    causes it to fall back on the original loader. This is definitely good for
    us since it means that even if we mess up here somehow, it shouldn't
    prevent the original module from being loaded. It will just be loaded
    without our rewrites.
    """
    code = compile(source, filename, "exec", dont_inherit=True)
    exec(code, module.__dict__)


class RewriterSettings:
    enable_concat: bool = False
    enable_fstring: bool = False
    enable_cformat_modulo: bool = False

    def __init__(
        self,
        enable_concat: bool = False,
        enable_fstring: bool = False,
        enable_cformat_modulo: bool = False,
    ):
        self.enable_concat = enable_concat
        self.enable_fstring = enable_fstring
        self.enable_cformat_modulo = enable_cformat_modulo

    @classmethod
    def default(cls, override_check: bool = False):
        enable_concat = override_check or not concat_works()
        enable_fstring = override_check or not fstring_works()
        enable_cformat_modulo = override_check or not cformat_modulo_works()

        return cls(
            enable_concat=enable_concat,
            enable_fstring=enable_fstring,
            enable_cformat_modulo=enable_cformat_modulo,
        )


class ContrastMetaPathFinder(importlib.abc.MetaPathFinder):
    settings: RewriterSettings

    def __init__(self, settings: RewriterSettings):
        self.settings = settings

    @fail_loudly("Unexpected error in find_spec - will not rewrite this module")
    def find_spec(self, fullname, path, target=None):
        """
        The finder is in charge of finding a module's "spec". The spec includes import
        machinery metadata about the module - including its name, source file path, and
        the loader, among others.

        Here, we first use importlib's default machinery to get the spec for the module
        about to be imported. The problem with this spec is that it also uses the
        default loader, which isn't what we want. To get around this, we reuse some
        metadata and generate a new spec that points at our loader.

        It's possible that this is needlessly complicated. It's a first-pass
        implementation, so we can (and should) refactor this as we learn more.
        """
        default_spec = importlib.machinery.PathFinder.find_spec(fullname, path)

        if not default_spec:
            logger.debug(
                "WARNING: no spec found for module - fullname=<%s>, path=<%s>",
                fullname,
                path,
            )
            return None

        default_spec_origin = getattr(default_spec, "origin", "") or ""
        if not default_spec_origin.endswith(".py"):
            logger.debug(
                "Will not rewrite non *.py file - fullname=<%s>, path=<%s>",
                fullname,
                default_spec_origin,
            )
            return None

        spec = importlib.util.spec_from_file_location(
            fullname,
            default_spec.origin,
            loader=ContrastRewriteLoader(self.settings),
            submodule_search_locations=default_spec.submodule_search_locations,
        )
        if spec is None:
            return spec

        loader = getattr(spec, "loader", None)

        if loader and not isinstance(loader, _ImportHookChainedLoader):
            spec.loader = _ImportHookChainedLoader(loader)

        return spec


class ContrastRewriteLoader(importlib.abc.Loader):
    settings: RewriterSettings

    def __init__(self, settings: RewriterSettings):
        self.settings = settings

    def create_module(self, _):
        """returning None uses the default behavior, which is fine"""
        return None

    def exec_module(self, module: types.ModuleType) -> None:
        """
        This method is responsible for actually doing the module `exec`-ing. We take
        control of this system and do the following:
        - read the original source file. We require pyc caching to be disabled for this
        - parse the source file into an AST
        - rewrite the AST
        - compile the AST into a code object
        - exec the code object

        Note that we add our custom add function to the module's globals. This prevents
        the need for import rewriting entirely
        """
        with scope.contrast_scope():
            original_source_code = None
            filename = module.__spec__.origin

            # May be None in some cases such as for namespace packages
            if filename is None:
                return

            try:
                with open(filename) as f:
                    original_source_code = f.read()

                tree = ast.parse(original_source_code)
            except Exception as ex:
                logger.debug("WARNING: failed to rewrite %s", filename, exc_info=ex)

                _load_module(original_source_code, module, filename)

                return

            if contrast__add.__name__ not in module.__dict__:
                try:
                    populate_rewritten_functions(module.__dict__)
                    PropagationRewriter(self.settings).visit(tree)
                    ast.fix_missing_locations(tree)
                except Exception as ex:
                    logger.debug("WARNING: failed to rewrite %s", filename, exc_info=ex)
            else:
                logger.debug(
                    "WARNING: contrast__add is already defined in %s; will not rewrite",
                    filename,
                )

            _load_module(tree, module, filename)


class PropagationRewriter(ast.NodeTransformer):
    settings: RewriterSettings

    @classmethod
    def with_default_settings(cls, override_check: bool = False):
        return cls(settings=RewriterSettings.default(override_check=override_check))

    def __init__(self, settings: RewriterSettings):
        self.settings = settings

    def _with_context(self, node, context):
        node = copy.copy(node)
        node.ctx = context
        return node

    def visit_BinOp(self, binop: ast.BinOp):
        """
        If we see an "Add" or a "Mod" binary operation, replace it with a call to our custom add/modulo
        function, which includes all necessary instrumentation.
        """
        binop.left = self.visit(binop.left)
        binop.right = self.visit(binop.right)

        if self.settings.enable_cformat_modulo and isinstance(binop.op, ast.Mod):
            binop_replacement = ast.Call(
                func=ast.Name(id="contrast__cformat__modulo", ctx=ast.Load()),
                args=[binop.left, binop.right],
                keywords=[],
            )

            ast.copy_location(binop_replacement, binop)
            return binop_replacement

        if not self.settings.enable_concat:
            return binop

        if not isinstance(binop.op, ast.Add):
            return binop

        binop_replacement = ast.Call(
            func=ast.Name(id="contrast__add", ctx=ast.Load()),
            args=[binop.left, binop.right],
            keywords=[],
        )
        ast.copy_location(binop_replacement, binop)
        return binop_replacement

    def visit_AugAssign(self, node: ast.AugAssign):
        """
        If we see an "Append", `+=` operation, rewrite it as a `+`.
        """
        node.value = self.visit(node.value)

        if not self.settings.enable_concat:
            return node

        if not isinstance(node.op, ast.Add):
            return node

        target = left = None
        if isinstance(node.target, ast.Name):
            name = ast.Name(id=node.target.id)
            target = self._with_context(name, ast.Store())
            left = self._with_context(name, ast.Load())
        else:
            target = node.target
            left = self._with_context(target, ast.Load())

        call_contrast_append_node = ast.Assign(
            targets=[target],
            value=ast.Call(
                func=ast.Name(id="contrast__append", ctx=ast.Load()),
                args=[self.visit(left), node.value],
                keywords=[],
            ),
        )

        ast.copy_location(call_contrast_append_node, node)
        # Recurse here in order to properly rewrite the `+` operation
        return call_contrast_append_node

    def visit_JoinedStr(self, node: ast.JoinedStr):
        if not self.settings.enable_fstring:
            return node

        return ast.Call(
            func=ast.Name(id="contrast__fstring", ctx=ast.Load()),
            args=node.values,
            keywords=[],
        )


@fail_loudly("Unexpected error concat_works", log_level="debug", return_value=False)
def concat_works():
    """
    Tests to see if concat via hooks patches works in this environment
    by running a str concat test as if we were in a request.

    Return: True if propagation happened, False otherwise.

    TODO: PYT-2678 Remove when concat hooks are finally removed
    """
    logger.debug("Testing if concat works.")

    with scope.pop_contrast_scope():
        one = "one"
        two = "two"
        track_and_tag(one)

        context = RequestContext(test_environ)
        with contrast.CS__CONTEXT_TRACKER.lifespan(context):
            res = one + two

    properties = contrast.STRING_TRACKER.get(res)
    result = properties is not None

    clear_properties()
    return result


@fail_loudly(
    "Unexpected error cformat_modulo_works", log_level="debug", return_value=False
)
def cformat_modulo_works():
    """
    Tests to see if modulo string/bytes formatting via hooks patches works in this environment
    by running a test as if we were in a request.

    Return: True if propagation happened, False otherwise.

    TODO: PYT-2710 Remove when cformat hooks are finally removed
    """
    logger.debug("Testing if modulo string/byte formatting works.")

    with scope.pop_contrast_scope():
        fmt = "%s %s"
        args = ("foo", "bar")
        track_and_tag(args[0])

        context = RequestContext(test_environ)
        with contrast.CS__CONTEXT_TRACKER.lifespan(context):
            res = fmt % args  # pylint: disable=string-format-interpolation

    properties = contrast.STRING_TRACKER.get(res)
    result = properties is not None

    clear_properties()
    return result


@fail_loudly("Unexpected error fstring_works", log_level="debug", return_value=False)
def fstring_works():
    """
    TODO: PYT-2679 Remove when fstring hooks are finally removed
    """
    logger.debug("Testing if fstring works.")

    with scope.pop_contrast_scope():
        string = "whatever"
        track_and_tag(string)

        context = RequestContext(test_environ)
        with contrast.CS__CONTEXT_TRACKER.lifespan(context):
            result = f"hello {string}!"

    properties = contrast.STRING_TRACKER.get(result)
    result = properties is not None

    clear_properties()
    return result


def register(override_settings=False, override_check=False):
    """
    Register our rewriter with the import system. After this call, any newly imported
    modules (from source code) will use our custom rewriter.

    Note that because this function is defined in the same module that defines our add
    replacement function, we never have to worry about rewriting the addition in the
    replacement function itself. If that were to occur, we would get an infinite
    recursion.

    Rewriter should only run in >=py3.10 and only in environments in which our default
    patching mechanism does not work.

    :param override_settings: Force the rewriter to be registered regardless of settings (for testing purposes)
    """
    settings = Settings()

    if not (settings.is_rewriter_enabled or override_settings):
        logger.debug("Rewriter disabled exiting setup")
        return

    rewriter_settings = RewriterSettings.default(override_check=override_check)
    sys.meta_path.insert(0, ContrastMetaPathFinder(rewriter_settings))

    settings.rewriter_enabled = True

    logger.debug("enabled AST rewriter")


def deregister():
    """
    Remove our rewriter from the import system. Modules that were loaded by our rewriter
    will remain rewritten.

    Return True if we find and deregister our machinery, False otherwise.
    """
    for i, finder in enumerate(sys.meta_path.copy()):
        if isinstance(finder, ContrastMetaPathFinder):
            sys.meta_path.pop(i)
            # Do we need to set settings.rewriter_enabled = False here?
            return True
    return False
