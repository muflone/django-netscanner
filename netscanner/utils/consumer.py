##
#     Project: Django NetScanner
# Description: A Django application to make network scans
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2019 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import multiprocessing
import types


class Consumer(multiprocessing.Process):
    """
    Consumer object to perform an action over any item in the tasks
    queue and save the results in the results queue
    """
    def __init__(self,
                 tasks_queue: multiprocessing.JoinableQueue,
                 results_queue: multiprocessing.Queue,
                 action: types.FunctionType) -> None:
        multiprocessing.Process.__init__(self)
        self.tasks = tasks_queue
        self.results = results_queue
        # Action to perform for each item
        self.action = action

    def run(self) -> None:
        """
        Process the data in the tasks queue until a stopper value is
        found and save the results into the results queue
        """
        while True:
            # Get an item from the queue to process
            item = self.tasks.get()
            # If the item is the stopper value, break the cycle
            if item is None:
                self.tasks.task_done()
                break
            # Get the result from the action and put into the queue
            result = self.action(item)
            self.results.put((item, result))
            self.tasks.task_done()
        return
