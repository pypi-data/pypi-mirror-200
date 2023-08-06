# bareimport - Import a python file even if it does not end in ".py".

This module is useful for building tests of functions within standalone scripts.
This allows you to have a standalone script file, without having to name it ending in
".py".  Then you can create test files that:

    import bareimport
    mod = bareimport.import_script_as_module('mod', ['./mod', '../mod'])
    
    #  You can also import "mod" now:
    from mod import func

## License

CC0 1.0 Universal, see LICENSE file for more information.

<!-- vim: ts=4 sw=4 ai et tw=85
-->
