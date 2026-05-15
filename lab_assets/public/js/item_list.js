frappe.listview_settings['Item'] = {
    onload: function(listview) {
        // Clear any existing filters (like "Last Updated On")
        listview.filter_area && listview.filter_area.clear();
    },

    refresh: function(listview) {
        // Hide filter button
        listview.page.wrapper.find('.filter-button').hide();

        // Hide filter chips area (VERY IMPORTANT)
        listview.page.wrapper.find('.filter-area').hide();
    }
};