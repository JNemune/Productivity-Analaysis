import os
from importlib import import_module

import matplotlib.pyplot as plt
import pandas as pd
from django import setup
from django.conf import settings
from matplotlib.ticker import FuncFormatter

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
my_settings = import_module("Configs.settings")
settings.configure(
    DATABASES=my_settings.DATABASES,
    INSTALLED_APPS=my_settings.INSTALLED_APPS,
    SECRET_KEY="django-insecure-&im0r5g-55jgm3r5y71n-)!_q#1s*1d0%en#1a(amut@332x5*",
)
setup()

from DB.models import Label, Session


# Helper function to convert minutes to HH:MM format
def minutes_to_hhmm(minutes, pos=None):
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"


# Function to convert RGB to hex color format
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


# Step 1: Define a color mapping dictionary using RGB values provided
color_mapping = {
    0: (238, 154, 154),
    1: (255, 151, 145),
    2: (255, 204, 128),
    3: (255, 236, 178),
    4: (255, 245, 156),
    5: (230, 238, 155),
    6: (194, 255, 166),
    7: (105, 240, 174),
    8: (128, 203, 196),
    9: (128, 222, 234),
    10: (129, 213, 250),
    11: (100, 181, 246),
    12: (158, 168, 219),
    13: (179, 157, 219),
    14: (207, 147, 217),
    15: (244, 143, 177),
    16: (188, 171, 164),
    17: (245, 245, 245),
    18: (224, 224, 224),
    19: (158, 158, 158),
    "unlabeled": (255, 255, 255),  # Added color for unlabeled
}

# Convert the color mapping to hex format
color_mapping_hex = {key: rgb_to_hex(value) for key, value in color_mapping.items()}


# Step 2: Extract session data and label color mapping
def get_label_colorid_mapping():
    return {label.title: label.colorid for label in Label.objects.all()}


label_colorid_mapping = get_label_colorid_mapping()

data = []
for session in Session.objects.all():
    weeknumber = session.datetime.weeknumber()  # Get the week number
    label = (
        "unlabeled" if session.label is None else session.label.title
    )  # Change null label to unlabeled
    duration = session.duration
    data.append([weeknumber, label, duration])

# Step 3: Create a pandas DataFrame for easier manipulation
df = pd.DataFrame(data, columns=["weeknumber", "label", "duration"])

# Step 4: Pivot the data to group by weeknumber and label
pivot_df = df.pivot_table(
    index="weeknumber", columns="label", values="duration", aggfunc="sum", fill_value=0
)

# Step 5: Create a list of colors corresponding to each label in the pivot table using the label color mapping
bar_colors = [
    color_mapping_hex[label_colorid_mapping.get(label, "unlabeled")]
    for label in pivot_df.columns
]

# Step 6: Plot the stacked bar chart using the label-specific colors
ax = pivot_df.plot(kind="bar", stacked=True, color=bar_colors, figsize=(15, 9))

# Step 7: Annotate each bar segment with duration values in HH:MM format
for week_index, week_data in enumerate(pivot_df.index):
    cumulative_sum = 0  # Reset the cumulative sum for each week
    for label in pivot_df.columns:
        duration = pivot_df.loc[week_data, label]
        if duration > 0:
            cumulative_sum += duration
            hhmm_duration = minutes_to_hhmm(duration)
            ax.text(
                week_index,
                cumulative_sum - (duration / 2),
                hhmm_duration,
                ha="center",
                va="center",
                fontsize=8,
                color="black",
                fontweight="bold",
            )

# Step 8: Annotate total duration above the topmost bar in HH:MM format
totals = pivot_df.sum(axis=1)
for week_index, total in enumerate(totals):
    hhmm_total = minutes_to_hhmm(total)
    ax.text(
        week_index,
        total + 0.5,
        hhmm_total,
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color="black",
    )

# Apply the custom formatter to the y-axis
ax.yaxis.set_major_formatter(FuncFormatter(minutes_to_hhmm))
plt.ylabel("Total Duration (HH:MM)")

# Step 9: Customize the plot
plt.title("Session Durations by Weeknumber and Label")
plt.xlabel("Weeknumber")
plt.ylabel("Total Duration (HH:MM)")
plt.xticks(rotation=0)
plt.legend(title="Label", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()

# Step 10: Show the plot
plt.savefig("weekly_analaysis.png")
