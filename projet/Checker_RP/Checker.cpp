#include<iostream>
#include<string>
#include<fstream>
#include<sstream>
#include<iomanip>
#include<stdlib.h>

#include"Instance.h"

using namespace std;


int main(int argc,char**argv){

  string nameext, namesol;
  double percent;

  if(argc!=4){
    cerr<<"usage: "<<argv[0]<<" <file percent sol>"<<endl;
    cerr<<"    Instance file of the Google Hash Code PhotoSlideShow (*.txt)"<<endl;
    cerr<<"    Percent of the number of photo to be read"<<endl;
    cerr<<"    Solution file to check"<<endl;
    return 1;
  }

  nameext=argv[1];
  percent=atof(argv[2]);
  namesol=argv[3];

  ifstream fic(nameext.c_str());
  if (fic==NULL){
    cerr<<"file "<<nameext<<" "<<" not found"<<endl;
    return 1;
  }

  Instance I(fic,percent);
  fic.close();

  I.sort_tags();
  cout<<endl<<endl;

  ifstream fic2(namesol.c_str());
  Sol S1(&I,fic2);
  if (fic2==NULL){
    cerr<<"file "<<namesol<<" "<<" not found"<<endl;
    return 1;
  }

  cout<<endl<<"Eval= "<<S1.eval()<<endl;

  return 0;

}


