unit Unit5;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Menus;

type
  TForm5 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    Button3: TButton;
    MainMenu1: TMainMenu;
    cb1: TMenuItem;
    N1: TMenuItem;
    N2: TMenuItem;
    N3: TMenuItem;
    N4: TMenuItem;
    N5: TMenuItem;
    N6: TMenuItem;
    N7: TMenuItem;
    N8: TMenuItem;
    N9: TMenuItem;
    Button4: TButton;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure N5Click(Sender: TObject);
    procedure N6Click(Sender: TObject);
    procedure TPrihodClick(Sender: TObject);
    procedure N8Click(Sender: TObject);
    procedure Button3Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form5: TForm5;

implementation

uses Unit1, Unit2, Postav, Prihod, Zapros;

{$R *.dfm}

procedure TForm5.Button1Click(Sender: TObject);
begin
form2.show();
end;

procedure TForm5.Button2Click(Sender: TObject);
begin
TPostav.show();
end;

procedure TForm5.N5Click(Sender: TObject);
begin
form2.show();
end;

procedure TForm5.N6Click(Sender: TObject);
begin
TPostav.show();
end;

procedure TForm5.TPrihodClick(Sender: TObject);
begin
TPrihod.show();
end;

procedure TForm5.N8Click(Sender: TObject);
begin
TPrihod.show();
end;

procedure TForm5.Button3Click(Sender: TObject);
begin
Tzapros.show();
end;

end.                                                                                                             ]=
