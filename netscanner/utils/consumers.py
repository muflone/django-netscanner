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

from .consumer import Consumer


class Consumers(object):
    def __init__(self,
                 tasks_queue: multiprocessing.Queue) -> None:
        """
        Consumers object to collect many Consumer objects to consume
        the data in the tasks queue.
        The results will be saved in the results queue.
        """
        self.tasks = tasks_queue
        self.results = multiprocessing.Queue()

    def execute(self,
                runners: int,
                action: types.FunctionType) -> None:
        """
        Instance a number of Consumer objects defined by runner and
        for each one execute the action function.
        The tasks queue is automatically join to wait the completion.
        All the results at the end can be find in the results queue.
        """
        # Define consumers
        for _ in range(1, runners + 1):
            # Create a new Consumer object and start it
            Consumer(tasks_queue=self.tasks,
                     results_queue=self.results,
                     action=action).start()
            # For each consumer add a stopper value to exit from loop
            self.tasks.put(None)
        # Wait until the the queue is empty
        self.tasks.join()

    def results_as_list(self) -> list:
        """
        Consume the results queue and convert it to a list
        """
        results = []
        while not self.results.empty():
            result = self.results.get()
            # Skip any empty value
            if result:
                results.append(result)
        return results
