import parted

class PartitionSetup(object):
    name = ""
    label = ""    
    type = ""
    format_as = None
    mount_as = None    
    partition = None
    aggregatedPartitions = []

    def __init__(self, partition):
        self.partition = partition
        self.size = partition.getSize()
        self.start = partition.geometry.start
        self.end = partition.geometry.end
        self.description = ""
        self.used_space = ""
        self.free_space = ""

        if partition.number != -1:
            self.name = partition.path   
            self.label = partition.name
            if self.label is None or self.label == "":
                self.label = self.name
         
            if partition.fileSystem is None:
                # no filesystem, check flags
                if partition.type == parted.PARTITION_SWAP:
                    self.type = ("Linux swap")
                elif partition.type == parted.PARTITION_RAID:
                    self.type = ("RAID")
                elif partition.type == parted.PARTITION_LVM:
                    self.type = ("Linux LVM")
                elif partition.type == parted.PARTITION_HPSERVICE:
                    self.type = ("HP Service")
                elif partition.type == parted.PARTITION_PALO:
                    self.type = ("PALO")
                elif partition.type == parted.PARTITION_PREP:
                    self.type = ("PReP")
                elif partition.type == parted.PARTITION_MSFT_RESERVED:
                    self.type = ("MSFT Reserved")
                elif partition.type == parted.PARTITION_EXTENDED:
                    self.type = ("Extended Partition")
                elif partition.type == parted.PARTITION_LOGICAL:
                    self.type = ("Logical Partition")
                elif partition.type == parted.PARTITION_FREESPACE:
                    self.type = ("Free Space")
                else:
                    self.type = ("Unknown")
            else:
                self.type = partition.fileSystem.type
        else:
            self.type = ""
            self.name = "unallocated"

    def add_partition(self, partition):
        self.aggregatedPartitions.append(partition)
        self.size = self.size + partition.getSize()
        self.end = partition.geometry.end
    
    def print_partition(self):
        print "Device: %s, format as: %s, mount as: %s" % (self.partition.path, self.format_as, self.mount_as)
