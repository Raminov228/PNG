#-------------------#
# Aminov Renat      #
# B02-002           #
#-------------------#

# v.0.0.2
#
# - Made zlib parser
#

class PNG():

    # @
    # Returns a cortage (name(str), content(list)) for adding it to a self.png dict
    #
    # input:   int         | start byte of chunk
    # output:  (str, list) | cortage with chunk's data
    # @
    def __init__(self, name_of_file):
        self.data = self.parse_png_to_hex(name_of_file)
        self.png = dict()
        self.png['HEADER'] = self._get_header()
        sb = 8
        while sb < len(self.data):
            chunk = self._get_chunk(sb)
            length = len(chunk[1])
            self.png.update([chunk])
            sb += 12 + length

    # @
    # Returns size of picture
    #
    # output:  (int, int) | cortage with size
    # @
    def get_size(self):
        height = self._trans_to_int(self.png['IHDR'][:4])
        width  = self._trans_to_int(self.png['IHDR'][4:8])
        return height, width

    def _get_comp_data(self):
        return self.png['IDAT'][2:]

    # @
    # Returns dict() with CINFO, CM, FLEVEL, FDICT, FCHECK
    #
    # output: {name: value}
    # @
    def _get_zlib(self):
        data = self.png['IDAT'][:2]
        data = ''.join([bin(int(d, 16))[2:].zfill(8) for d in data])
        zlib = dict()
        zlib['CINFO'] = data[:4]
        zlib['CM'] = data[4:8]
        zlib['FLEVEL'] = data[8:10]
        zlib['FDICT'] = data[10:11]
        zlib['FCHECK'] = data[11:16]
        return zlib

    # @
    # Transforms hex to int
    #
    # input:   [hex]       | list of hexes
    # output:  int         | int
    # @
    def _trans_to_int(self, bytes_array):
        return int('0x' + ''.join(bytes_array), 0)

    # @
    # Transforms hex to string
    #
    # input:   [hex]       | list of hexes
    # output:  str         | str
    # @
    def _trans_to_string(self, bytes_array):
        b = bytes.fromhex(''.join(bytes_array))
        return b.decode('utf-8')

    # @
    # Returns a cortage (name(str), content(list)) for adding it to a self.png dict
    #
    # input:   int         | start byte of chunk
    # output:  (str, list) | cortage with chunk's data
    # @
    def _get_chunk(self, start_byte):
        name = self._get_name_of_chunk(start_byte)
        content = self._get_content_of_chunk(start_byte)
        chunk = (name, content)
        return chunk

    # @
    # Returns a list of str's view of hex byte
    #
    # input:   str  | name of file
    # output:  list | str(hex)
    # @
    def parse_png_to_hex(self, name_of_file):
        with open(name_of_file, 'rb') as f:
            data = f.readlines()

        hex_data = []
        for i in data:
            hex_data += [str(i.hex()[j * 2] + i.hex()[j * 2 + 1]) for j in range(int(len(i.hex()) / 2))]
        return hex_data

    # @
    # Returns a length of chunk's content. It takes first 4th bytes of chunk and make an int
    #
    # input:  int | index of chunk's start byte
    # output: int | length of content
    # @
    def _get_length_of_chunk(self, start_byte):
        return self._trans_to_int(self.data[start_byte : start_byte + 4])

    # @
    # Returns a chunk's name. chunk[4:8] -> str()
    #
    # input:  int | index of chunk's start byte
    # output: str | chunk's name
    # @
    def _get_name_of_chunk(self, start_byte):
        return self._trans_to_string(self.data[start_byte + 4 : start_byte + 8])

    # @
    # Returns a chunk's content. chunk[8 : 8 + len(chunck)] -> str()
    #
    # input:  int  | index of chunk's start byte
    # output: list | hex list
    # @
    def _get_content_of_chunk(self, start_byte):
        l = self._get_length_of_chunk(start_byte)
        return self.data[start_byte + 8: start_byte + 8 + l]

    # @
    # Returns a header (first 8 bytes)
    #
    # output: list | hex list
    # @
    def _get_header(self):
        return self.data[:8]


png = PNG('test.png')
for name in png.png:
    print(name, png.png[name])


print(png.get_size())
print(png._get_zlib())
print(png._get_comp_data())