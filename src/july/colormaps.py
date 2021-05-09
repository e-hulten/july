import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


def tups2cmap(tups_list, reverse=False):
    cmap = [list(tup) for tup in tups_list]
    cmap = [[x / 255 for x in lst] for lst in cmap]
    return cmap if not reverse else cmap[::-1]


cmaps_list = plt.colormaps()
cmaps_dict = dict(zip(cmaps_list, cmaps_list))

july_lst = [
    (204, 71, 71, 255),
    (230, 97, 97, 255),
    (255, 122, 122, 255),
    (255, 141, 130, 255),
    (255, 161, 138, 255),
    (254, 187, 152, 255),
    (252, 204, 162, 255),
    (249, 217, 174, 255),
    (246, 232, 182, 255),
    (245, 238, 186, 255),
    (255, 255, 212, 255),
    (255, 255, 237, 255),
]
cmaps_dict["july_r"] = LinearSegmentedColormap.from_list("", tups2cmap(july_lst))
cmaps_dict["july"] = LinearSegmentedColormap.from_list("", tups2cmap(july_lst, True))

github_list = [
    (235, 237, 240, 255),
    (155, 233, 168, 255),
    (64, 196, 99, 255),
    (48, 161, 78, 255),
    (33, 110, 57, 255),
]
cmaps_dict["github"] = ListedColormap(tups2cmap(github_list))
cmaps_dict["github_r"] = ListedColormap(tups2cmap(github_list, True))

sunset_list = [
    (255, 229, 119, 255),
    (254, 192, 81, 255),
    (255, 136, 102, 255),
    (253, 96, 81, 255),
    (57, 32, 51, 255),
]
cmaps_dict["sunset"] = LinearSegmentedColormap.from_list("", tups2cmap(sunset_list))
cmaps_dict["sunset_r"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(sunset_list, True)
)

dark_golden_list = [
    (254, 192, 54, 255),
    (217, 126, 13, 255),
    (165, 48, 6, 255),
    (111, 1, 0, 255),
    (36, 0, 2, 255),
]
cmaps_dict["dark_golden"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(dark_golden_list)
)
cmaps_dict["dark_golden_r"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(dark_golden_list, True)
)

golden_hour_list = [
    (254, 253, 242, 255),
    (254, 252, 231, 255),
    (254, 244, 199, 255),
    (255, 237, 166, 255),
    (252, 220, 135, 255),
    (253, 189, 109, 255),
    (246, 160, 100, 255),
    (225, 152, 109, 255),
    (189, 110, 71, 255),
    (166, 92, 65, 255),
]
cmaps_dict["golden_hour"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(golden_hour_list)
)
cmaps_dict["golden_hour_r"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(golden_hour_list, True)
)

golden_list = [
    (255, 254, 253, 255),
    (254, 247, 205, 255),
    (254, 238, 170, 255),
    (253, 217, 116, 255),
    (253, 197, 93, 255),
    (254, 167, 80, 255),
    (237, 143, 76, 255),
    (203, 114, 68, 255),
    (182, 97, 66, 255),
    (144, 78, 62, 255),
    (129, 76, 61, 255),
]
cmaps_dict["golden"] = LinearSegmentedColormap.from_list("", tups2cmap(golden_list))
cmaps_dict["golden_r"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(golden_list, True)
)

pastel_sunrise_list = [
    (188, 133, 163, 255),
    (254, 173, 185, 255),
    (249, 225, 224, 255),
    (151, 153, 186, 255),
    (72, 123, 166, 255),
]

cmaps_dict["pastel_sunrise"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(pastel_sunrise_list)
)
cmaps_dict["pastel_sunrise_r"] = LinearSegmentedColormap.from_list(
    "", tups2cmap(pastel_sunrise_list, True)
)
