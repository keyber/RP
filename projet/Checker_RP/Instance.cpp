#include"Instance.h"
#include<iostream>
#include<sstream>
#include<fstream>
#include<iomanip>
#include<stdlib.h>

void aff_list(list<string>&l){
 list<string>::const_iterator it;
 for (it=l.begin();it!=l.end();it++)
   cout<<*it<<" ";
 cout<<endl;
}

int min(int a, int b, int c){
  if (a<=b)
    if (a<=c) return a;
    else return c; 
  else
    if (c<=b) return c;
    else return b;
}

int eval_slide(const list<string> &l1, const list<string> &l2){
  int a=0,b=0,c=0;
  list<string>::const_iterator it1,it2;
  
  it1=l1.begin();
  it2=l2.begin();
  while ((it1!=l1.end())&&(it2!=l2.end())){
    if (*it1<*it2) {
      a++;
      it1++;
    }
    else
      if (*it2<*it1){
	c++;
	it2++;
      }
      else {
	b++;
	it1++;
	it2++;
      }
  }
  if (it1==l1.end())
    while (it2!=l2.end()){
      c++;
      it2++;
    }
  if (it2==l2.end())
    while (it1!=l1.end()){
      a++;
      it1++;
    }        
  
  return min(a,b,c);
}

void concat_sorted_without_double(const list<string>&l1,const list<string>&l2,list<string>&l){
  l.clear();
  list<string>::const_iterator it1,it2;

  it1=l1.begin();
  it2=l2.begin();
  while ((it1!=l1.end())&&(it2!=l2.end())){
    if (*it1<*it2) {
      l.push_back(*it1);
      it1++;
    }
    else
      if (*it2<*it1){
	l.push_back(*it2);
	it2++;
      }
      else {
	l.push_back(*it1);
	it1++;
	it2++;
      }
  }
  if (it1==l1.end())
    while (it2!=l2.end()){
      l.push_back(*it2);
      it2++;
    }
  if (it2==l2.end())
    while (it1!=l1.end()){
      l.push_back(*it1);
      it1++;
    }        
    

  
}


///////////////////////////
///////////////////////////


Instance::Instance(istream &f, double p){
  int i,q,j;
  string s;

  f>>nbphot;
  nbphot=p*nbphot/100;

  V.resize(nbphot);
  
  for (i=0;i<nbphot;i++){
    f>>V[i].ori;
    f>>q;
    for (j=0;j<q;j++){
      f>>s;
      V[i].tags.push_back(s);
    }
  }

}

void Instance::sort_tags(){
  int i;
    for (i=0;i<nbphot;i++)
      V[i].tags.sort();
}

void Instance::aff(ostream &o){
  int i;
  list<string>::const_iterator it;
  
  o<<nbphot<<endl;
  for (i=0;i<nbphot;i++){
    o<<V[i].ori<<" "<<V[i].tags.size()<<" ";
    for (it=V[i].tags.begin();it!=V[i].tags.end();it++)
      o<<*it<<" ";
    o<<endl;
  }
  
}

int Instance::search_closer(list<string>&l, vector<bool> &mark){
  int i, max,val,maxi;
  max=-1;maxi=-1;
  for (i=0;i<nbphot;i++){
    if (!(mark[i])){
      val=eval_slide(l,V[i].tags);
      if (max<val){
	max=val;
	maxi=i;
      }
    }
  }
  return maxi;
}

int Instance::search_closerV(list<string>&l, vector<bool> &mark){
  int i, max,val,maxi;
  max=-1;maxi=-1;
  for (i=0;i<nbphot;i++){
    if ((!(mark[i]))&&(V[i].ori=='V')){
      val=eval_slide(l,V[i].tags);
      if (max<val){
	max=val;
	maxi=i;
      }
    }
  }
  return maxi;
}


//////////////////////////////////////////
//////////////////////////////////////////

Sol::Sol(Instance *II,istream & f){
  int i;
  vector<bool> mark;
  
  I=II;

  mark.resize(I->nbphot);
  for (i=0;i<I->nbphot;i++) mark[i]=false;
  
  f>>nbslides;
  vsol.resize(nbslides);

  if (nbslides<=0){
    cerr<<"Error first line: at least 1 slide needed"<<endl;
    exit(1);
  }

  for (i=0;i<nbslides;i++){
    f>>vsol[i].p1;
    if ((vsol[i].p1>I->nbphot)||(mark[vsol[i].p1]==true)){
      cerr<<"Ligne "<<i+1<<" : "<<"wrong number or photo used twice"<<endl;
      exit(1);
    }
    mark[vsol[i].p1]=true;
    if (I->V[vsol[i].p1].ori=='H')
      vsol[i].p2=-1;
    else{
      f>>vsol[i].p2;
      if ((vsol[i].p2>I->nbphot)||(mark[vsol[i].p2]==true)){
	cerr<<"Ligne "<<i+1<<" : "<<"wrong number or photo used twice"<<endl;
	exit(1);
      }
      mark[vsol[i].p2]=true;
      
    }
  }
}


void Sol::aff(ostream &o){
  int i;
  o<<nbslides<<endl;
  for (i=0;i<nbslides;i++){
    o<<vsol[i].p1<<" ";
    if (vsol[i].p2!=-1) o<<vsol[i].p2;
    o<<endl;
  }

}

double Sol::eval(){
  int i;
  list<string> *l1,*l2;
  list<string> L1,L2;
  double val=0;
  
  for (i=0;i<nbslides-1;i++){
    if (vsol[i].p2==-1) l1=&(I->V[vsol[i].p1].tags);
    else{
      concat_sorted_without_double(I->V[vsol[i].p1].tags,I->V[vsol[i].p2].tags,L1);
      l1=&L1;
    }
    if (vsol[i+1].p2==-1) l2=&(I->V[vsol[i+1].p1].tags);
    else{
      concat_sorted_without_double(I->V[vsol[i+1].p1].tags,I->V[vsol[i+1].p2].tags,L2);
      l2=&L2;
    }

    val=val+eval_slide(*l1,*l2);
     
    
  }

  return val;

}
  
    
