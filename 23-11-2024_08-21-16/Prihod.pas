unit Prihod;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, DB, mySQLDbTables, ExtCtrls, DBCtrls, Grids, DBGrids, StdCtrls,
  Mask;

type
  TTPrihod = class(TForm)
    DBGrid1: TDBGrid;
    DBNavigator1: TDBNavigator;
    MySQLDatabase1: TMySQLDatabase;
    MySQLTable1: TMySQLTable;
    DataSource1: TDataSource;
    MySQLTable2: TMySQLTable;
    DataSource2: TDataSource;
    MySQLTable1idprihod: TAutoIncField;
    MySQLTable1idtovar: TIntegerField;
    MySQLTable1datPrih: TDateField;
    MySQLTable1kolvo: TIntegerField;
    MySQLTable1idpostav: TIntegerField;
    MySQLTable1namepostav: TStringField;
    MySQLTable3: TMySQLTable;
    MySQLTable1nametovar: TStringField;
    DBEdit1: TDBEdit;
    DBEdit2: TDBEdit;
    DBLookupComboBox1: TDBLookupComboBox;
    DBLookupComboBox2: TDBLookupComboBox;
    DataSource3: TDataSource;
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  TPrihod: TTPrihod;

implementation

{$R *.dfm}

end.
