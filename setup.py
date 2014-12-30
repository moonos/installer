class Setup(object):
    language = None
    timezone = None
    timezone_code = None
    keyboard_model = None    
    keyboard_layout = None    
    keyboard_variant = None    
    partitions = [] #Array of PartitionSetup objects
    username = None
    hostname = None
    autologin = False
    password1 = None
    password2 = None
    real_name = None    
    grub_device = None
    disks = []
    target_disk = None
    gptonefi = False
    # Optionally skip all mouting/partitioning for advanced users with custom setups (raid/dmcrypt/etc)
    # Make sure the user knows that they need to:
    #  * Mount their target directory structure at /target
    #  * NOT mount /target/dev, /target/dev/shm, /target/dev/pts, /target/proc, and /target/sys
    #  * Manually create /target/etc/fstab after init_install has completed and before finish_install is called
    #  * Install cryptsetup/dmraid/mdadm/etc in target environment (using chroot) between init_install and finish_install
    #  * Make sure target is mounted using the same block device as is used in /target/etc/fstab (eg if you change the name of a dm-crypt device between now and /target/etc/fstab, update-initramfs will likely fail)
    skip_mount = False
    
    #Descriptions (used by the summary screen)    
    keyboard_model_description = None
    keyboard_layout_description = None
    keyboard_variant_description = None
    
    def print_setup(self):
        if __debug__:
            print "-------------------------------------------------------------------------"
            print "language: %s" % self.language
            print "timezone: %s (%s)" % (self.timezone, self.timezone_code)        
            print "keyboard: %s - %s (%s) - %s - %s (%s)" % (self.keyboard_model, self.keyboard_layout, self.keyboard_variant, self.keyboard_model_description, self.keyboard_layout_description, self.keyboard_variant_description)        
            print "user: %s (%s)" % (self.username, self.real_name)
            print "autologin: ", self.autologin
            print "hostname: %s " % self.hostname
            print "passwords: %s - %s" % (self.password1, self.password2)        
            print "grub_device: %s " % self.grub_device
            print "skip_mount: %s" % self.skip_mount
            if (not self.skip_mount):
                print "target_disk: %s " % self.target_disk
                if self.gptonefi:
                    print "GPT partition table: True"
                else:
                    print "GPT partition table: False"
                print "disks: %s " % self.disks                       
                print "partitions:"
                for partition in self.partitions:
                    partition.print_partition()
            print "-------------------------------------------------------------------------"
