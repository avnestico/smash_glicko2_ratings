from RankingSettings import DefaultRating, DefaultRD, DefaultVol

"""
Copyright (c) 2009 Ryan Kirkman

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from math import *

class Player:
    # Class attribute
    # The system constant, which constrains
    # the change in volatility over time.
    _tau = 0.5

    def getRating(self):
        return (self.__rating * 173.7178) + 1500 

    def setRating(self, rating):
        self.__rating = (rating - 1500) / 173.7178

    rating = property(getRating, setRating)

    def getRd(self):
        return self.__rd * 173.7178

    def setRd(self, rd):
        self.__rd = rd / 173.7178

    rd = property(getRd, setRd)
     
    def __init__(self, rating = DefaultRating, rd = DefaultRD, vol = DefaultVol):
        # For testing purposes, preload the values
        # assigned to an unrated player.
        self.setRating(rating)
        self.setRd(rd)
        self.vol = vol
            
    def _preRatingRD(self):
        """ Calculates and updates the player's rating deviation for the
        beginning of a rating period.
        
        preRatingRD() -> None
        
        """
        self.__rd = sqrt(pow(self.__rd, 2) + pow(self.vol, 2))
        
    def update_player(self, rating_list, RD_list, outcome_list):
        """ Calculates the new rating and rating deviation of the player.
        
        update_player(list[int], list[int], list[bool]) -> None
        
        """
        # Convert the rating and rating deviation values for internal use.
        rating_list = [(x - 1500) / 173.7178 for x in rating_list]
        RD_list = [x / 173.7178 for x in RD_list]

        v = self._v(rating_list, RD_list)
        self.vol = self._newVol(rating_list, RD_list, outcome_list, v)
        self._preRatingRD()
        
        self.__rd = 1 / sqrt((1 / pow(self.__rd, 2)) + (1 / v))
        
        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * \
                       (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        self.__rating += pow(self.__rd, 2) * tempSum

    def _newVol(self, rating_list, RD_list, outcome_list, v, epsilon=0.000001):
        """ Calculating the new volatility as per the Glicko2 system.
        
        _newVol(list, list, list) -> float
        
        """
        delta = self._delta(rating_list, RD_list, outcome_list, v)
        tau = self._tau
        rd = self.__rd

        # 1. Let a = ln(s^2), and define f(x)
        a = log(self.vol ** 2)

        def f(x):
            tmp = rd ** 2 + v + exp(x)
            b = exp(x) * (delta ** 2 - tmp) / (2 * tmp ** 2)
            c = (x - a) / tau ** 2
            return b - c

        # 2. Set the initial values of the iterative algorithm.
        x0 = a
        if delta ** 2 > rd ** 2 + v:
            x1 = log(delta ** 2 - rd ** 2 - v)
        else:
            k = 1
            if f(a - k * tau) < 0:
                k += 1
            x1 = a - k * tau

        # 3. Let fA = f(A) and f(B) = f(B)
        f_x0, f_x1 = f(x0), f(x1)

        # 4. While |B-A| > e, carry out the following steps.
        while abs(x0 - x1) > epsilon:
            # (a) Let C = A + (A - B)fA / (fB-fA), and let fC = f(C).
            x2 = x0 + (x0 - x1) * f_x0 / (f_x1 - f_x0)
            f_x2 = f(x2)
            # (b) If fCfB < 0, then set A <- B and fA <- fB; otherwise, just set
            #     fA <- fA/2.
            if f_x1 * f_x2 < 0:
                x0, f_x0 = x1, f_x1
            else:
                f_x0 /= 2
            # (c) Set B <- C and fB <- fC.
            x1, f_x1 = x2, f_x2
            # (d) Stop if |B-A| <= e. Repeat the above three steps otherwise.

        # 5. Once |B-A| <= e, set s' <- e^(A/2)
        return exp(x1 / 2)
        
    def _delta(self, rating_list, RD_list, outcome_list, v):
        """ The delta function of the Glicko2 system.
        
        _delta(list, list, list) -> float
        
        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempSum += self._g(RD_list[i]) * (outcome_list[i] - self._E(rating_list[i], RD_list[i]))
        return v * tempSum
        
    def _v(self, rating_list, RD_list):
        """ The v function of the Glicko2 system.
        
        _v(list[int], list[int]) -> float
        
        """
        tempSum = 0
        for i in range(len(rating_list)):
            tempE = self._E(rating_list[i], RD_list[i])
            tempSum += pow(self._g(RD_list[i]), 2) * tempE * (1 - tempE)
        return 1 / tempSum
        
    def _E(self, p2rating, p2RD):
        """ The Glicko E function.
        
        _E(int) -> float
        
        """
        return 1 / (1 + exp(-1 * self._g(p2RD) * \
                                 (self.__rating - p2rating)))
        
    def _g(self, RD):
        """ The Glicko2 g(RD) function.
        
        _g() -> float
        
        """
        return 1 / sqrt(1 + 3 * pow(RD, 2) / pow(pi, 2))
        
    def did_not_compete(self):
        """ Applies Step 6 of the algorithm. Use this for
        players who did not compete in the rating period.

        did_not_compete() -> None
        
        """
        self._preRatingRD()
