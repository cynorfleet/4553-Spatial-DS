import pprint as pp
import os,sys
import glob

class FileHelper(object):
    def __init__(self,directory):
        self.directory = directory
        self.data_by_borough = glob.glob(self.directory+'data_by_borough/*.csv')
        self.data_by_crime = glob.glob(self.directory+'data_by_crime/*.csv')

    def get_data(self,borough=None,crime=None):
        data = []

        assert borough is not None or crime is not None

        if borough is not None:
            assert borough.lower() in ['bronx','manhattan','queens','brooklyn','staten_island']
        if crime is not None:
            assert crime.lower() in ['larceny','assault','drugs','fraud','harrassment']

        if borough is not None:
            for file in self.data_by_borough:
                if borough.lower() in file.lower():
                    data.extend(self._read_file(file,crime))
        elif crime is not None:
            for file in self.data_by_crime:
                if crime.lower() in file.lower():
                    data.extend(self._read_file(file,borough))
        else:
            return []

        return data
    
    def _read_file(self,filename,key):
        data = []
        with open(filename) as f:
            for line in f:
                line = ''.join(x if i % 2 == 0 else x.replace(',', ':') for i, x in enumerate(line.split('"')))
                if key is not None:
                    if key.lower() in line.lower():
                        data.append(line.strip().split(','))
                else:
                    data.append(line.strip().split(','))
        return data

if __name__=='__main__':
    fh = FileHelper('/code/repos/4553-Spatial-DS/Resources/NYPD_CrimeData/')
    data = fh.get_data(borough='manhattan',crime='larceny')
