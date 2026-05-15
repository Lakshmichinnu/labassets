import frappe


@frappe.whitelist()
def get_asset_category_chart():

    chart_data = frappe.db.sql("""

        SELECT

            location,
            asset_category,
            COUNT(name) as total

        FROM
            `tabAsset`

        GROUP BY
            location,
            asset_category

        ORDER BY
            location

    """, as_dict=True)

    labs = []
    categories = []

    for row in chart_data:

        if row.location not in labs:

            labs.append(row.location)

        if row.asset_category \
        not in categories:

            categories.append(
                row.asset_category
            )

    datasets = []

    for category in categories:

        values = []

        for lab in labs:

            total = 0

            for row in chart_data:

                if (
                    row.location == lab
                    and
                    row.asset_category
                    == category
                ):

                    total = row.total

            values.append(total)

        datasets.append({

            "name": category,

            "values": values

        })

    return {

        "labels": labs,

        "datasets": datasets

    }