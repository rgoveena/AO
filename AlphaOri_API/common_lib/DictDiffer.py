import pprint

################################################################################
# Class    :   DictDiffer
# Purpose  :   To compare a dictionary of settings and show any differences.
#
# Created  :   9/25/2017
# Copyright:   Alpha Ori Ltd (c) 2017
# License  :
#
################################################################################

class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, past_dict, current_dict):
        """constructor"""

        self.current_dict = current_dict
        self.past_dict = past_dict

        self.set_current = set(current_dict.keys())
        self.set_past = set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)


    def DumpData(self, input_data, title=None):

        pp = pprint.PrettyPrinter(indent=2)                                     # setup prettyprinter object

        if title:                                                               # output titles - if given
            print("%s") % title

        pp.pprint(input_data)                                                   # print the data to screen
        print
        print

    def added(self):
        """added - find which dict items have been added"""
        added_keys = self.set_current - self.intersect

        return self.get_delta_set(added_keys)


    def removed(self):
        """removed - find which dict items have been removed"""

        removed_keys = self.set_past - self.intersect

        return self.get_delta_set(removed_keys)


    def changed(self):
        """changed - find which dict items have been changed"""

        changed_keys = set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])

        return self.get_delta_set(changed_keys)


    def unchanged(self):
        """unchanged - find which dict items have been unchanged"""

        unchanged_keys = set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

        return self.get_delta_set(unchanged_keys)


    def get_delta_set(self, delta_keys):
        """find the dict delta values"""

        temp_dict = {}

        try:
            for item in delta_keys:
                temp_dict[item] = self.current_dict[item]
        except KeyError:
            temp_dict[item] = "Key NOT Found In Set : %s" % item

        return temp_dict


    def all_diffs(self):
        """Show all of the different values in one dictionary"""

        all_diff_dict = {}

        temp_dict = self.added()            # ADDED VALUES

        if temp_dict:                       # only add if there are values
            all_diff_dict["Added Values"] = temp_dict


        temp_dict = self.changed()          # CHANGED VALUES

        if temp_dict:                       # only add if there are values
            all_diff_dict["Modified Values"] = temp_dict


        temp_dict = self.removed()          # REMOVED VALUES

        if temp_dict:                       # only add if there are values
            all_diff_dict["Removed Values"] = temp_dict


        return all_diff_dict                # return all of the differences
