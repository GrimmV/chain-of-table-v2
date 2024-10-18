few_shot_individual_op = {
    "plan_add_column_demo": """If the table does not have the needed column to tell whether the statement is True or False, we use f_add_column() to add a new column for it. For example,
    /*
    col : rank | lane | player | time
    row 1 :  | 5 | olga tereshkova (kaz) | 51.86
    row 2 :  | 6 | manjeet kaur (ind) | 52.17
    row 3 :  | 3 | asami tanno (jpn) | 53.04
    */
    Statement: there are one athlete from japan.
    Function: f_add_column(country of athlete)
    Explanation: The statement is about the number of athletes from japan. We need to known the country of each athlete. There is no column of the country of athletes. We add a column "country of athlete".""",

    "plan_select_column_demo": """If the table only needs a few columns to tell whether the statement is True or False, we use f_select_column() to select these columns for it. For example,
    /*
    col : code | county | former province | area (km2) | population | capital
    row 1 : 1 | mombasa | coast | 212.5 | 939,370 | mombasa (city)
    row 2 : 2 | kwale | coast | 8,270.3 | 649,931 | kwale
    row 3 : 3 | kilifi | coast | 12,245.9 | 1,109,735 | kilifi
    */
    Statement: momasa is a county with population higher than 500000.
    Function: f_select_column(county, population)
    Explanation: The statement wants to check momasa county with population higher than 500000. We need to know the county and its population. We select the column "county" and column "population".""",

    "plan_select_row_demo": """If the table only needs a few rows to tell whether the statement is True or False, we use f_select_row() to select these rows for it. For example,
    /*
    table caption : jeep grand cherokee.
    col : years | displacement | engine | power | torque
    row 1 : 1999 - 2004 | 4.0l (242cid) | power tech i6 | - | 3000 rpm
    row 2 : 1999 - 2004 | 4.7l (287cid) | powertech v8 | - | 3200 rpm
    row 3 : 2002 - 2004 | 4.7l (287cid) | high output powertech v8 | - | -
    row 4 : 1999 - 2001 | 3.1l diesel | 531 ohv diesel i5 | - | -
    row 5 : 2002 - 2004 | 2.7l diesel | om647 diesel i5 | - | -
    */
    Statement: the jeep grand cherokee with the om647 diesel i5 had the third lowest numbered displacement.
    Function: f_select_row(row 1, row 4, row 5)
    Explanation: The statement wants to check the om647 diesel i5 had third lowest numbered displacement. We need to know the first three low numbered displacement and all rows that power is om647 diesel i5. We select the row 1, row 4, row 5.""",


    "plan_group_column_demo": """If the statement is about items with the same value and the number of these items, we use f_group_column() to group the items. For example,
    /*
    col : district | name | party | residence | first served
    row 1 : district 1 | nelson albano | dem | vineland | 2006
    row 2 : district 1 | robert andrzejczak | dem | middle twp. | 2013†
    row 3 : district 2 | john f. amodeo | rep | margate | 2008
    */
    Statement: there are 5 districts are democratic
    Function: f_group_column(party)
    Explanation: The statement wants to check 5 districts are democratic. We need to know the number of dem in the table. We group the rows according to column "party".""",

    "plan_sort_column_demo": """If the statement is about the order of items in a column, we use f_sort_column() to sort the items. For example,
    /*
    col : position | club | played | points
    row 1 : 1 | malaga cf | 42 | 79
    row 10 : 10 | cp merida | 42 | 59
    row 3 : 3 | cd numancia | 42 | 73
    */
    Statement: cd numancia placed in the last position.
    Function: f_sort_column(position)
    Explanation: The statement wants to check about cd numancia in the last position. We need to know the order of position from last to front. We sort the rows according to column "position"."""
}
