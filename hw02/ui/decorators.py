# import time
#
#
# def wait(method, error=Exception, timeout=10, interval=1, check=False, **kwargs):
#     st = time.time()
#     while time.time() - st < timeout:
#         try:
#             result = method(**kwargs)
#             if check:
#                 if result:
#                     return result
#             else:
#                 return result
#         except error:
#             pass
#         time.sleep(interval)
#     raise TimeoutError("Timeout was reached during operation '%s'. See details in debug log" % method.__name__)
