from charmhelpers.core.hookenv import (
    action_get,
    action_fail,
    action_set,
    config,
    status_set,
)

from charms.reactive import (
    remove_state as remove_flag,
    set_state as set_flag,
    when,
    when_not,
)
import charms.sshproxy
from subprocess import (
    Popen,
    CalledProcessError,
    PIPE,
)

import time 

@when_not('ubuntuvnf.configured')
def not_configured():
    # If your charm has other dependencies before it can install,
    # add those as @when() clauses above., or as additional @when()
    # decorated handlers below
    # See the following for information about reactive charms:
    #  * https://jujucharms.com/docs/devel/developer-getting-started
    #  * https://github.com/juju-solutions/layer-basic#overview
    config_changed()

@when('config.changed', 'sshproxy.configured')
def config_changed():
    cfg = config()
    """Verify the configuration.
    Verify that the charm can be accessed via SSH
    This code will credentials explicitely in juju status just for testing purposes
    They can be removed by deleting the + credentials addon
    """
    credentials = " with " + cfg['ssh-hostname'] + "-" + cfg['ssh-username'] + "-" + cfg['ssh-password']
    status_set('maintenance', 'Verifying configuration data' + credentials)
    (validated, output) = charms.sshproxy.verify_ssh_credentials()
    if not validated:
        status_set('blocked', 'Unable to verify SSH credentials' + credentials)
        return
    if validated:
        set_flag('ubuntuvnf.configured')
        status_set('active', 'ready ' + credentials)
        return
    status_set('blocked', 'Waiting for configuration')

# two when clauses work like an AND
@when('config.changed')
@when_not('sshproxy.configured')
def invalid_credentials():
    status_set('blocked', 'Waiting for SSH credentials.')
    pass

# say-hello sample action
# two when clauses work like an AND
@when('ubuntuvnf.configured')
@when('actions.say-hello')
def say_hello():
    err = ''
    ## Gets the name parameter that the descriptor passed, otherwise the defined by default in actions.yaml
    param1 = "Hello " + action_get("name")
    try:
        # Put the code here that you want to execute, it includes parameters
        # Parameters should be defined in both actions.yaml and the VNF descriptor
        ## Define the command to run
        cmd = "sudo wall -n " + param1
        ## Run the command through SSH
        result, err = charms.sshproxy._run(cmd)
    except:
        # In case it fails, throw an exception
        action_fail('command failed:' + err)
    else:
        # In case it suceeds, return the output
        action_set({'output': result})
    finally:
        # Finally, end the action by removing the flag
        remove_flag('actions.say-hello')   

# two when clauses work like an AND
@when('ubuntuvnf.configured')
@when('actions.start')
def start():
    err = ''
    try:
        # Put the code here that you want to execute automatically when VNF starts
        # this will further validate that SSH works and otherwise trigger a new config_changed event... TBC
        cmd = "sudo ls"
        result, err = charms.sshproxy._run(cmd)
    except:
        action_fail('command failed:' + err)
    else:
        action_set({'output': result})
    finally:
        remove_flag('actions.start')