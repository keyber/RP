#ifndef __INSTANCE_H__
#define __INSTANCE_H__

#include<iostream>
#include<string>
#include<list>
#include<vector>

using namespace std;

class Photo{
 public:
  char ori;
  list<string> tags;
};

class Instance{
 public:
  int nbphot;
  vector<Photo> V;

  Instance(istream & f, double p);
  void aff(ostream &o);
  void sort_tags();

  int search_closer(list<string>&l,vector<bool> &mark);
  int search_closerV(list<string>&l,vector<bool> &mark);
 
};


class Slide{
 public:
  int p1,p2;  // p2==-1 if no photo
};

class Sol{
 public:
  Instance *I;
  int nbslides;
  vector<Slide> vsol;

  Sol(Instance *II,istream & f);
  void aff(ostream &o);
  double eval();

};


#endif
