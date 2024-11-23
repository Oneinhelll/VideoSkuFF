unit Postav;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, DB, mySQLDbTables, StdCtrls, Mask, DBCtrls, ExtCtrls, Grids,
  DBGrids, frxClass, frxDBSet, frxExportPDF;

type
  TTPostav = class(TForm)
    DBGrid1: TDBGrid;
    DBNavigator1: TDBNavigator;
    MySQLDatabase1: TMySQLDatabase;
    MySQLTable1: TMySQLTable;
    DataSource1: TDataSource;
    Button1: TButton;
    frxDBDataset1: TfrxDBDataset;
    frxReport1: TfrxReport;
    procedure Button1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  TPostav: TTPostav;

implementation

{$R *.dfm}

procedure TTPostav.Button1Click(Sender: TObject);
begin
frxReport1.ShowReport();
end;

end.
