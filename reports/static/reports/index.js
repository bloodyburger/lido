$(() => {
    let drillDownDataSource = {};
  
    $('#sales').dxPivotGrid({
      allowSortingBySummary: true,
      allowSorting: true,
      allowFiltering: true,
      allowExpandAll: true,
      showBorders: true,
      showRowGrandTotals: false,
      showColumnGrandTotals: false,
      fieldChooser: {
        enabled: true,
      },
      export: {
        enabled:true
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
      onExporting: function(e) { 
        var workbook = new ExcelJS.Workbook(); 
        var worksheet = workbook.addWorksheet('Main sheet'); 
        DevExpress.excelExporter.exportPivotGrid({ 
            worksheet: worksheet, 
            component: e.component,
            customizeCell: function(options) {
                var excelCell = options;
                excelCell.font = { name: 'Arial', size: 12 };
                excelCell.alignment = { horizontal: 'left' };
            } 
        }).then(function() {
            workbook.xlsx.writeBuffer().then(function(buffer) { 
                saveAs(new Blob([buffer], { type: 'application/octet-stream' }), 'PivotGrid.xlsx'); 
            }); 
        }); 
        e.cancel = true; 
    },
      dataSource: {
        fields: [
          /*{
          caption: 'primary_label',
          width: 120,
          dataField: 'primary_label',
          area: 'row',
        }, */{
          caption: 'secondary_label',
          dataField: 'secondary_label',
          width: 150,
          area: 'row',
        },
        {
          caption: 'account',
          dataField: 'account',
          width: 150,
          area: 'row',
        },
        {
          caption: 'category',
          dataField: 'category',
          width: 150,
          area: 'row',
        },
        {
          caption: 'subcategory',
          dataField: 'subcategory',
          width: 150,
          area: 'row',
        }, {
          dataField: 'period',
          dataType: 'date',
          area: 'column',
        }, {
          caption: 'value_eth',
          dataField: 'value_eth',
          dataType: 'number',
          summaryType: 'sum',
          format: 'currency',
          area: 'data',
        },
      // Filters
        {
          area: 'filter', 
          dataField: 'secondary_label',
          filterType: 'include',
          filterValues: ['1.1. Staked Assets', '3.2. Operating Performance']
      },
      {
        area: 'filter', 
        dataField: 'account',
        filterType: 'include',
        filterValues: ['3.2.1. Net Revenue', '3.2.2. Cost of Revenue','1.1.1. Staked ETH']
    }],
        store: sales,
      },
    });
  
    const salesPopup = $('#sales-popup').dxPopup({
      width: 1360,
      height: 600,
      //resizeEnabled:true,
      contentTemplate(contentElement) {
        $('<div />')
          .addClass('drill-down')
          .dxDataGrid({
            width: 1260,
            height: 500,
            scrolling: {
              mode: 'virtual',
            },
            export: {
              enabled:true,
              allowExportSelectedData: true
              },
              onExporting(e) {
                const workbook = new ExcelJS.Workbook();
                const worksheet = workbook.addWorksheet('LIDO');
          
                DevExpress.excelExporter.exportDataGrid({
                  component: e.component,
                  worksheet,
                  autoFilterEnabled: true,
                }).then(() => {
                  workbook.xlsx.writeBuffer().then((buffer) => {
                    saveAs(new Blob([buffer], { type: 'application/octet-stream' }), 'LIDO.xlsx');
                  });
                });
                e.cancel = true;
              },
            columns: ['period', 'primary_label', 'secondary_label', 'account','base_token_address','value_eth'],
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
  