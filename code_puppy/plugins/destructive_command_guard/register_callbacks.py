"""Callback registration for the destructive command guard plugin.

Hooks into the run_shell_command phase to intercept destructive shell
commands (rm -rf /, git reset --hard, docker system prune -af, etc.) and
prompt the user for approval before allowing them through.

Returns {"blocked": True} to deny, None to allow.
"""

from code_puppy.callbacks import register_callback

from code_puppy.plugins.destructive_command_guard.detector import (
    detect_destructive_command,
)

from code_puppy.plugins.guard_framework import(
    make_shell_guard,
    GuardSpec,
)

_DESTRUCTIVE_GUARD_SPEC = GuardSpec(                                                                                                                                                                                                            
    title="Destructive Command Guard ",                                                                                                                                                                                                         
    detected_label="Destructive command detected: ",                                                                                                                                                                                             
    consequence="This command could cause irreversible data loss",                                                                                                                                                                             
    block_advice="If you *really* need to run this, use your terminal directly",                                                                                                                                                             
    detect=detect_destructive_command,                                                                                                                                                                                                          
)                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                
destructive_command_guard_callback = make_shell_guard(_DESTRUCTIVE_GUARD_SPEC)                                                                                                                                                                  

def register() -> None:                                                                                                                                                                                                                         
    register_callback("run_shell_command", destructive_command_guard_callback)                                                                                                                                                                  
                                                                                                                                                                                                                                                
register()







