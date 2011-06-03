from dcdata.management.base.extractor import Extractor


class NimspExtractor(Extractor):

    IN_DIR       = '/home/datacommons/data/auto/lobbying/download/IN'
    DONE_DIR     = '/home/datacommons/data/auto/lobbying/download/DONE'
    REJECTED_DIR = '/home/datacommons/data/auto/lobbying/download/REJECTED'
    OUT_DIR      = '/home/datacommons/data/auto/lobbying/raw/IN'

    FILE_PATTERN = 'Sunlight.*.tar.gz'

    def __init__(self):
        super(NimspExtractor, self).__init__()


Command = NimspExtractor

