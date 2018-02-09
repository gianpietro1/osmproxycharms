# osmproxycharms
Sample proxy charms for the Open Source MANO platform

## ubuntuvnf
An single VDU VNF that instantiates an Ubuntu Xenial machine.  Its main primitive, 'say-hello', takes a 'name' parameter and shows a 'Hello [name]' output to all VM terminals through the 'wall' command.  This example can be further modified to send any command to a VNF with one or more parameters.  The VNF package includes a cloud-init file that sets the credentials to ubuntu/ubuntu.
The specific code for the 'say-hello' primitive can be found here: https://github.com/gianpietro1/osmproxycharms/blob/master/ubuntuvnf/ubuntuvnf_vnfd/charms/ubuntuvnf/reactive/ubuntuvnf.py#L65
