from pathlib import Path
import datetime

import pandas as pd
import xlwings as xw

xl_app = xw.apps.active

# Set workbook variables
wb: xw.Book = xw.Book.caller()
ws_voucher_maint: xw.Sheet = wb.sheets['Voucher Maintenance']
ws_settings: xw.Sheet = wb.sheets['Settings']
ws_summary: xw.Sheet = wb.sheets['Summary']
vouch_import_path = Path(ws_settings['c_vouch_import'].value)
shortpay_path = Path(ws_settings['c_shortpay_req'].value)
vouch_maint_path = Path(ws_settings['c_vouchMaint'].value)


def _ws_vouch_formulas():
    ws_voucher_maint['t_vouchMaint[Supplier-Name]'].value = '=IF([@[Supplier-Nr]]="","",XLOOKUP([@[Supplier-Nr]],t_suppliers[Supplier],t_suppliers[Sort Name],"Invalid Supplier-Nr"))'
    ws_voucher_maint['t_vouchMaint[Account-Description]'].value = '=IF([@Account]="","",XLOOKUP([@Account],t_accounts[Account],t_accounts[Description]))'
    ws_voucher_maint['t_vouchMaint[Sub-Account-Description]'].value = '=IF([@[Sub-Account]]="","",XLOOKUP([@[Sub-Account]],t_subAcnt[Sub-Account],t_subAcnt[Description]))'
    ws_voucher_maint['t_vouchMaint[Cost-Center-Description]'].value = '=IF([@[Cost-Center]]="","",XLOOKUP([@[Cost-Center]],t_costCenter[Cost-Center],t_costCenter[Description]))'
    ws_voucher_maint['t_vouchMaint[Entity]'].value = '="2000"'
    ws_voucher_maint['t_vouchMaint[Already-Vouchered]'].value = '=XLOOKUP([@Invoice],t_dataDetail[Invoice],t_dataDetail[Name],"")&"-"&TEXT(XLOOKUP([@Invoice],t_dataDetail[Invoice],t_dataDetail[Amount],""),"$#,##0.00")'


def button_export(user_name: str = 'Unknown_User'):
    df_vouch: pd.DataFrame = ws_voucher_maint['t_vouchMaint[[#All]]'].options(pd.DataFrame, index=False).value
    df_vouch_export = df_vouch[[
        'Invoice',
        'Supplier-Nr',
        'Date',
        'Account',
        'Sub-Account',
        'Cost-Center',
        'Entity',
        'Amount'
    ]]
    df_vouch_export = df_vouch_export.rename(columns={
        'Supplier-Nr': 'Supplier',
        'Account': 'Account_1',
        'Sub-Account': 'Sub-Acct_1',
        'Cost-Center': 'CC_1',
        'Entity': 'Enty_1',
        'Amount': 'Amount_1'
    })
    df_vouch_export = df_vouch_export.reindex(columns=[
        'Invoice',
        'Supplier',
        'Date',
        'Account_1',
        'Sub-Acct_1',
        'CC_1',
        'Project_1',
        'Enty_1',
        'Amount_1',
    ])

    vouch_total = df_vouch_export['Amount_1'].sum()
    df_vouch_export['Date'] = df_vouch_export['Date'].dt.strftime('%m/%d/%y')

    dttime_now = datetime.datetime.now()
    file_date = dttime_now.strftime('%m%d%y%H%M')
    supplier_nr = str(df_vouch_export['Supplier'].iloc[0])
    file_name_csv = 'vouch-' + user_name + '-' + file_date + '-' + supplier_nr + '.csv'
    file_name_excel = 'vouch-' + user_name + '-' + file_date + '-' + supplier_nr + '.xlsx'

    msgbox_return = xl_app.alert('Are you ready to continue?', title='Ready', mode='info', buttons='yes_no')
    if msgbox_return == 'yes':
        # Export
        # df_vouch_export.to_csv(vouch_import_path / file_name, index=False)
        df_vouch_export.to_csv(vouch_import_path / file_name_csv, index=False)
        df_vouch_export.to_excel(vouch_maint_path / file_name_excel, index=False)

        # Add to summary
        last_row = str(ws_summary.range('B' + str(ws_summary.cells.last_cell.row)).end('up').row + 1)
        ws_summary['B' + last_row].value = file_name_csv
        ws_summary['C' + last_row].value = dttime_now
        ws_summary['D' + last_row].value = vouch_total

        # Clear table
        ws_voucher_maint['t_vouchMaint[Invoice]'].clear_contents()
        ws_voucher_maint['t_vouchMaint[Supplier-Nr]'].clear_contents()
        ws_voucher_maint['t_vouchMaint[Date]'].clear_contents()
        ws_voucher_maint['t_vouchMaint[Account]'].clear_contents()
        ws_voucher_maint['t_vouchMaint[Sub-Account]'].clear_contents()
        ws_voucher_maint['t_vouchMaint[Cost-Center]'].clear_contents()
        ws_voucher_maint['t_vouchMaint[Amount]'].clear_contents()
        lr_vouch_maint = str(ws_voucher_maint.range('C' + str(ws_voucher_maint.cells.last_cell.row)).end('up').row)
        ws_voucher_maint['7:' + lr_vouch_maint].delete()
        _ws_vouch_formulas()

        xl_app.alert('Complete. File name: ' + file_name_csv, title='Complete', mode='info')


if __name__ == "__main__":
    # To debug:
    # ------------------------------------------------------------------
    # xw.Book('Voucher Maintenance.xlsb').set_mock_caller()
    # wb: xw.Book = xw.Book.caller()
    # ws_voucher_maint: xw.Sheet = wb.sheets['Voucher Maintenance']
    # ws_settings: xw.Sheet = wb.sheets['Settings']
    # ws_summary: xw.Sheet = wb.sheets['Summary']
    # vouch_import_path = Path(ws_settings['c_vouch_import'].value)
    # shortpay_path = Path(ws_settings['c_shortpay_req'].value)
    # vouch_maint_path = Path(ws_settings['c_vouchMaint'].value)
    # ------------------------------------------------------------------
    button_export()
