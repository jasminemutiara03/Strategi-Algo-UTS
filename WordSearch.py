"""
Menerapkan papan Pencarian Kata yang diberi daftar kata sebagai Array 2D.
Kelas ini dapat diimplementasikan sendiri tanpa WordBoard.py.

Setelah instantiasi, Array 2D berisi semua huruf papan
serta solusinya dapat diakses sebagai berikut:

word_search = WordSearch()
2d_board = word_search.board
solutions = word_search.solutions

Alex Eidt
"""

from random import choice, shuffle


class WordSearch:
    """
    Kelas WordSearch mengabstraksi papan Pencarian Kata sebagai larik 2D
    pertama diisi dengan semua kata yang diberikan dalam orientasi yang berbeda,
    lalu isi sisa ruang kosong dengan huruf acak.
    """

    def __init__(self, size, words):
        """
        Menginisialisasi instance kelas WordSearch.

        Parameter
            ukuran: Ukuran papan. Papan akan selalu berbentuk persegi berukuran x ukuran huruf
            kata-kata: Daftar kata yang akan disembunyikan dalam pencarian kata
        """
        self._size = size
        self._words = list(set(map(str.upper, words)))

        # Check to see if the longest word in the words list is
        # less than the size of the board + 2 to ensure that
        # all words can be successfully placed on the board.
        assert (
            self._size - max(map(len, self._words)) > 2
        ), f"Board Size {self._size} is too small."

        shuffle(self._words)
        self.board = [[None for _ in range(self._size)] for _ in range(self._size)]

        # Solutions is a mapping of words hidden in the board to a set of coordinates
        # of each letter in these words
        self.solutions = {}

        # Fill the board with words
        check = False
        while not check:
            self._init_board()
            check = self._fill_with_words()

        self._fill_board()

    def _get_orientation(self, word_len):
        """
        Mendapat orientasi dan titik awal dari sebuah kata.
        Mengacu pada koordinat awal (x, y) dan langkah (ox, oy)
        untuk kata yang diberikan.

        Parameters
            word_len: Panjang kata yang menjadi "statistik".
                      ditemukan untuk

        Returns
            Tuple yang berisi koordinat awal dan ukuran langkah
            dalam arah x dan y.
        """
        starty = startx = 0
        endy = endx = self._size

        orient = choice(range(0, 4))

        if orient == 0:  # Horizontal
            ox = 1
            oy = 0
            endx = self._size - word_len  # board columns - word_len
        elif orient == 1:  # Vertical Down
            ox = 0
            oy = 1
            endy = self._size - word_len  # board rows - word_len
        elif orient == 2:  # Upward Diagonal
            ox = 1
            oy = -1
            starty = word_len
            endx = self._size - word_len  # board columns - word_len
        elif orient == 3:  # Downward Diagonal
            ox = 1
            oy = 1
            endy = self._size - word_len
            endx = self._size - word_len  # board columns - word_len

        x = choice(range(startx, endx))
        y = choice(range(starty, endy))

        return x, y, ox, oy

    def _check_board(self, word, x, y, ox, oy):
        """
        Diberikan kata tertentu dengan koordinat awal (x, y) dan langkah
        ukuran dalam arah x dan y (ox, oy), menentukan apakah itu
        mungkin untuk menempatkan kata itu di koordinat tersebut di papan tulis.
        Parameters
            word: The word that could be placed at the given coordinates
            x: Starting x coordinate
            y: Starting y coordinate
            ox: Step size in x direction
            oy: Step size in y direction

        Returns
            True if the word can be placed at the proposed location, False
            otherwise.
        """
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            if self.board[y_coord][x_coord] != letter and self.board[y_coord][x_coord]:
                return False

        return True

    def _add_word(self, word):
        """
        Menambahkan kata ke papan Pencarian Kata.

        Parameters
            word: The word being placed on the Word Search Board.

        Returns
            Salah jika kata tidak bisa diletakkan di papan tulis (bertemu
            putaran tak terbatas). Benar jika kata itu bisa diletakkan di papan tulis.
        """
        x, y, ox, oy = self._get_orientation(len(word))
        # Check to see if the randomly picked location from getStats is
        # viable for the given word. If not, it will continue to check
        # until a spot has been found.

        # Count exists to prevent an infinite loop from occurring.
        # Especially with small board sizes, it's possible that due to
        # the random placement of the words, the algorithm runs out
        # of valid spots for the word. The way to solve this is to
        # arbitrarily choose a large number and check if the number
        # of iterations has exceeded it.
        count = 0
        while not self._check_board(word, x, y, ox, oy):
            x, y, ox, oy = self._get_orientation(len(word))
            count += 1
            # Check for infinite loop
            if count > 20000:
                return False

        self.solutions[word] = set()
        for i, letter in enumerate(word):
            x_coord = x + i * ox
            y_coord = y + i * oy
            self.board[y_coord][x_coord] = letter
            self.solutions[word].add((letter, x_coord, y_coord))

        return True

    def _fill_board(self):
        """
        
        Isi semua lokasi papan yang kosong dengan huruf acak.
        """
        for i in range(self._size):
            for j in range(self._size):
                if not self.board[i][j]:
                    self.board[i][j] = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def _init_board(self):
        """
        Menginisialisasi setiap lokasi papan menjadi Tidak Ada.
        """
        for i in range(self._size):
            for j in range(self._size):
                self.board[i][j] = None

    def _fill_with_words(self):
        """
        Isi papan dengan daftar kata yang diberikan.

        Pengembalian
            Salah jika salah satu kata tidak dapat ditambahkan ke papan tulis.
            Benar jika semua kata telah berhasil ditambahkan ke papan tulis.
        """
        for word in self._words:
            check = self._add_word(word)
            if not check:
                return False

        return True

    def __len__(self):
        """
        Mengembalikan panjang satu sisi papan.
        """
        return self._size

    def __str__(self):
        """
        Mengembalikan Papan Pencarian Kata sebagai String.
        """
        return "\n".join([" ".join(row) for row in self.board])
