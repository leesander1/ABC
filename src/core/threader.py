import threading

# class Threader(object):
#     '''
#     Threading class for the application
#     '''
#
#     def __init__(self):
#         self.threads = []
#
#     def startBackgroundThread(self, method, args=False):
#         '''
#         Start new thread
#         '''
#
#         if args:
#             newThread = threading.Thread(target=method, args=args)
#         else:
#             newThread = threading.Thread(target=method)
#
#         newThread.start()
#
#         self.threads.append(newThread)
#
#     def waitForThreads(self, timeout=5.00):
#         '''
#         Send stop signal to threads and wait for them to end
#         '''
#
#         for thread in self.threads:
#             thread.join(timeout)