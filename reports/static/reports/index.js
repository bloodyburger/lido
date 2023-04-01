$(() => {
    let drillDownDataSource = {};
  
    $('#sales').dxPivotGrid({
      allowSortingBySummary: true,
      allowSorting: true,
      allowFiltering: true,
      allowExpandAll: true,
      showBorders: true,
      showRowGrandTotals: false,
      fieldChooser: {
        enabled: false,
      },
      onCellClick(e) {
        if (e.area === 'data') {
          const pivotGridDataSource = e.component.getDataSource();
          const rowPathLength = e.cell.rowPath.length;
          const rowPathName = e.cell.rowPath[rowPathLength - 1];
          const popupTitle = `${rowPathName || 'Total'} Drill Down Data`;
  
          drillDownDataSource = pivotGridDataSource.createDrillDownDataSource(e.cell);
          salesPopup.option('title', popupTitle);
          salesPopup.show();
        }
      },
      dataSource: {
        fields: [{
          caption: 'primary_label',
          width: 120,
          dataField: 'primary_label',
          area: 'row',
        }, {
          caption: 'secondary_label',
          dataField: 'secondary_label',
          width: 150,
          area: 'row',
        }, {
          dataField: 'period',
          dataType: 'date',
          area: 'column',
        }, {
          caption: 'value_usd',
          dataField: 'value_usd',
          dataType: 'number',
          summaryType: 'sum',
          format: 'currency',
          area: 'data',
        }],
        store: sales,
      },
    });
  
    const salesPopup = $('#sales-popup').dxPopup({
      width: 1400,
      height: 600,
      contentTemplate(contentElement) {
        $('<div />')
          .addClass('drill-down')
          .dxDataGrid({
            width: 1860,
            height: 500,
            scrolling: {
              mode: 'virtual',
            },
            columns: ['period', 'primary_label', 'secondary_label', 'account','base_token_address','value_eth','value_usd'],
          })
          .appendTo(contentElement);
      },
      onShowing() {
        $('.drill-down')
          .dxDataGrid('instance')
          .option('dataSource', drillDownDataSource);
      },
      onShown() {
        $('.drill-down')
          .dxDataGrid('instance')
          .updateDimensions();
      },
    }).dxPopup('instance');
  });
  