from collections import deque, UserString

from .base_models import Context as Ctx
from .get_lattice import FCASolver, Inclose
from .utils.utils import to_subscript
from .plot.plot import plot_from_hasse


class RelationalAttribute(UserString):
    def __init__(self, p, relation=None, concepts=None):
        """
        :param p: the p18n operator or a string, in which case the relation and concepts are expected to be None.
                  This is mainly to maintain the idea of string[:2] in which another string is expected as a return.
        :param relation: the relation instance
        :param concepts: a list of tuples (lattice_id, concept_id, concept)
        """
        if isinstance(p, str):
            super().__init__(p)
        else:
            value = f'{p}{relation} : {self._concepts_subscripts(concepts)}'
            self.concepts = concepts
            super().__init__(value)

    def _concepts_subscripts(self, combination):
        return ",".join(
            [f'C{to_subscript(lattice_idx)}₋{to_subscript(c_idx)}' for lattice_idx, c_idx, _ in combination])


class Context(Ctx):
    def __init__(self, O, A, I, solver: FCASolver = None):
        super().__init__(O, A, I)

        if solver is None:
            solver = Inclose()

        self.solver = solver
        self.iteration = 0

        # for each relation, we know what are the attributes already added
        self._relational_attributes = {}

        # FIXME: The ideal would be to cache the last_lattice
        #        and also calculate them from the point they were already calculated
        #        * is that possible not to repeat calculations?
        #        * if not, can we bound the amount of calculations that have to be repeated?
        self._last_lattice = None

    def get_concepts(self):
        return self.solver.get_concepts(self)

    def get_lattice(self):
        hasse, concepts = self.solver.get_lattice(self)
        if self._last_lattice is None:
            self._last_lattice = Lattice(hasse, concepts)
        else:
            self._last_lattice = Lattice(hasse, concepts)
        return self._last_lattice

    def get_association_rules(self, **kwargs):
        return self.solver.get_association_rules(self, **kwargs)

    def graduate(self, relation, p, lattices):
        """
        Applies graduation. Extends the formal context with more attributes
        with the relation `relation`, using the p18n operator, against the lattices `lattices` (a list of lattice, lattice_idx)
        """
        for combination in self._tuple_iterator(lattices, 0):
            key = RelationalAttribute(p, relation, combination)
            if key not in self._relational_attributes:
                self.A.append(key)
                self._relational_attributes[key] = len(
                    self.A) - 1  # adding the idx of the attribute

            attribute_idx = self._relational_attributes[key]
            have_to_add_column = attribute_idx > len(self.I[0]) - 1
            for o, relations in enumerate(self.I):
                has_attribute = p(
                    o, relation, [
                        concept for _, _, concept in combination])
                if have_to_add_column:
                    relations.append(has_attribute)
                else:
                    relations[attribute_idx] = has_attribute

        self.iteration += 1

    def _tuple_iterator(self, lattices, i):
        current_lattice_idx = lattices[i][0]
        current_lattice = lattices[i][1]
        if i == len(lattices) - 1:
            for c_idx, concept in enumerate(current_lattice.concepts):
                yield deque([(current_lattice_idx, c_idx, concept)])
        else:
            for c_idx, concept in enumerate(current_lattice.concepts):
                for combination in self._tuple_iterator(lattices, i + 1):
                    combination.appendleft(
                        (current_lattice_idx, c_idx, concept))
                    yield combination


class Lattice:
    def __init__(self, hasse, concepts, from_iteration=None):
        self.hasse = hasse
        self.concepts = concepts
        self.ctx = self.concepts[-1].context

    def isomorph(self, other_lattice):
        """
        This method needs the two lattices to have the concepts ordered in the same way, othetwise it'll fail
        - Complexity: O(|self.concepts|), \\omega(1)
        """
        if len(self.concepts) != len(other_lattice.concepts):
            return False

        for i, concept in enumerate(self.concepts):
            if len(concept.O) != len(other_lattice.concepts[i].O) or \
               len(concept.A) != len(other_lattice.concepts[i].A):
                return False
        return True

    def plot(self, **kwargs):
        return plot_from_hasse(self.hasse, self.concepts, **kwargs)

    def __repr__(self):
        return str(self.concepts)
