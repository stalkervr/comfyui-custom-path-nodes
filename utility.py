# class AnyConcatenation:
#     """Node to concatenate two inputs of type ANY with an optional separator and newline."""
#
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {},
#             "optional": {
#                 "any_1": ("STRING", {"default": ""}),
#                 "any_2": ("STRING", {"default": ""}),
#                 "separator": ("STRING", {"default": ",,"}),
#                 "newline": ("BOOLEAN", {"default": False}),
#             }
#         }
#
#     RETURN_TYPES = ("STRING",)
#     RETURN_NAMES = ("STRING",)
#     FUNCTION = "concatenate_inputs"
#     CATEGORY = "Stalkervr/Utility"
#
#     def concatenate_inputs(self, any_1="", any_2="", separator="", newline=False):
#         # Преобразуем входы в строки для конкатенации
#         str_input1 = str(any_1)
#         str_input2 = str(any_2)
#
#         if newline:
#             concatenated_output = f"{str_input1}{separator}\n{str_input2}"
#         else:
#             concatenated_output = f"{str_input1}{separator}{str_input2}"
#
#         return (concatenated_output,)