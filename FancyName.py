#!/usr/bin/env python3
from MediatorBuilder import MediatorBuilder

class FancyName:
	def run(self):
		mediatorBuilder = MediatorBuilder()
		mediatorBuilder.construct()
		self._mediator = mediatorBuilder.mediator

		self._mediator.crawl()
		print('----Fancy Name Ende-----')


if __name__ == '__main__':
	FancyName().run()
