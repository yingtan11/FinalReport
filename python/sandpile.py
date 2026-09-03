import numpy as np
import scipy as sp
import scipy.spatial


class SandPile:
    """SandPile class"""

    def __init__(self, width, height, threshold=4):
        """Initialize a sandpile with the specified width and height."""
        self.width = width
        self.height = height
        self.threshold = threshold

        self.grid = np.zeros((width, height), dtype=int)

        # We may want to keep track of the overall mass of the sand pile
        # overtime.  The following array will store the masses at each time
        # step (so that `len(self.mass_history)` is equal to the number of time
        # steps the sand pile has been running).
        self.mass_history = []
        # You probably will want to define other attributes to store statistics.

        # It is good practice to define *all* class attributes in the
        # `__init__` function, even if they get redefined later.  You may want
        # to define variables which are used to keep track of avalanches.

    def drop_sand(self, n=1, site=None):
        """Add `n` grains of sand to the grid.  Each grains of sand is added to
        a random site.

        This function also increments the time by 1 and update the internal
        `mass_history`.  Depending on how you want to code things, you may wish
        to also run the avalanche (alternatively, the avalanching might be
        executed elsewhere).

        Parameters
        ==========

        n: int

          The number of grains of sand of drop at this time step.  If left
          unspecified, defaults to 1.

        site:

          The site on which the grain(s) of sand should be dropped.  If `None`,
          a random site is used.

        """

        if site is None:
            rng = np.random.default_rng()
            site = rng.integers(low = 0, high = [self.width, self.height])
        x = site[0]
        y = site[1]
        self.grid[x][y] += n

        self.mass_history.append(self.mass())


    def mass(self):
        """Return the mass of the grid."""
        return np.sum(self.grid)

    def topple(self, site):
        """Topple the specified site."""
        x, y = site
        self.grid[x][y] -= 4
        if x+1 < self.width:
            self.grid[x+1][y] += 1
        if x-1 >= 0:    
            self.grid[x-1][y] += 1
        if y+1 < self.height:
            self.grid[x][y+1] += 1
        if y-1 >=0:
            self.grid[x][y-1] += 1

    def avalanche(self, start):
        """Run the avalanche causing all sites to topple and store the stats of
        the avalanche in the appropriate variables.
        """
        to_topple = []
        # checks first
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] >= self.threshold:
                    to_topple.append((x, y))

        # cause avalanche
        for site in to_topple:
            self.topple(site)
            print(self.grid)
            self.avalanche(start)

    # You are free (and encouraged) to define more methods within this class

pile = SandPile(3, 3)
print(pile.grid)
print(pile.mass())

# figure 3
pile.grid[0, 0] = pile.grid[2, 1] = pile.grid[2, 2] = 1
pile.grid[1, 0] = pile.grid[1, 2] = pile.grid[2, 0] = 2
pile.grid[0, 1] = pile.grid[0, 2] = 3
pile.grid[1, 1] = 4
print(pile.grid)
print(pile.mass())

pile.avalanche(None)
print(pile.grid)
print(pile.mass_history)