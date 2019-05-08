#include <random>

#include <iostream>
#include <string>
#include <fstream>
#include <stdio.h>
#include <string.h>
#include <vector>
// random_shuffle example
#include <algorithm>    // std::random_shuffle
#include <ctime>        // std::time
#include <cstdlib>      // std::rand, std::srand
#include <math.h>
using namespace std;

#define ISTNIEJE 0
#define RED 1
#define GREEN 2
#define BLUE 3
#define DECYZJA 4
#define KCK 5
#define PARAMS_CNT 6
const int height=2336;
const int width=3504;
//zmienna zawierajaca obraz
int tab[height][width][PARAMS_CNT];

string folder=R"(C:\Users\vulws\PycharmProjects\DnoOka\txt\)";

string naglowek="odleglosc od srodka;27x27ziel;1x1ziel;27x27b;1x1b;czy nie jest brzegowy;twoje KCK;DECYZJA \n";
//nie napisze dzisiaj tego dijkstry
vector<vector<float>> blankParams;
vector<vector<float>> veinParams;
vector<float> current;
int x,y;

vector<int> ranges{27,1};//musi być malejaco



//kolory, edytujesz poprzez zmiane ranges
vector<vector<float>> colorRanges(vector<int> pos){
    vector<int> colors{GREEN,BLUE};
    vector<vector<float>> wynik;
    vector<vector<int>> dzielniki;
    for (int i=0;i<colors.size();i++) {
        wynik.emplace_back();
        dzielniki.emplace_back();
        for(int j=0;j<ranges.size();j++){
            wynik[i].push_back(0);
            dzielniki[i].push_back(0);
        }
    }
    for (int i=-ranges[0]/2;i<=ranges[0]/2;i++){
        for(int j=-ranges[0]/2;j<=ranges[0]/2;j++){
            if(pos[0]+i<0||pos[0]+i>=height||pos[1]+j<0||pos[1]+j>=width) continue;
            if(!(tab[pos[0]+i][pos[1]+j][ISTNIEJE>0])) continue;

            for (int k=0;k<ranges.size();k++){
             if (i>=-ranges[k]/2&&i<=ranges[k]/2&&j>=-ranges[k]/2&&j<=ranges[k]/2){
                 for( int l=0;l<colors.size();l++){
                     wynik[l][k]+=tab[pos[0]+i][pos[1]+j][colors[l]];
                     dzielniki[l][k]++;
                 }
             }
             else break;
         }
        }
    }
    for (int k=0;k<ranges.size();k++) {
    for (int l = 0; l < colors.size(); l++) {
        wynik[l][k]=(float)wynik[l][k]/(dzielniki[l][k]*255);
    }}
    int l=colors.size()-1,k=0;
    wynik[l].push_back((float)dzielniki[l][k]/(ranges[k]*ranges[k])*3.0/4.0+0.25);//razy 4 dla
    return wynik;
}

vector<float> appendWynik(vector<float> wynik,vector<vector<float>> dodawany){
    for(int i=0;i<dodawany.size();i++){
        for(int j=0;j<dodawany[i].size();j++){
            wynik.push_back(dodawany[i][j]);
        }
    }
}

//to edytujesz, dodaj nową funckję zwracajacą wektor wektorow i appenduj tak jak kolory
vector<float> generateParams(vector<int> pos){
    vector<float> wynik;
    wynik.push_back((float)(abs(pos[0]-height/2)+abs(pos[1]-width/2))/((float)height/2+(float)width/2));
    vector<vector<float>> kolory;
    kolory = colorRanges(pos);
    wynik=appendWynik(wynik,kolory);
    wynik.push_back((float) tab[pos[0]][pos[1]][KCK]);
    // to zrobiłem na szybko nietestowane (linijka wyzej i funkcja appendWynik, oryginal ponizej)
//    for(int i=0;i<kolory.size();i++){
//        for(int j=0;j<kolory[i].size();j++){
//            wynik.push_back(kolory[i][j]);
//        }
//    }
    return wynik;
}

//to zostaw
int main() {
    srand ( unsigned ( time(nullptr) ) );
    string typ[3]={"dr","h","g"};
    for (int ii=5;ii<16;ii++){
        for (int jj=0;jj<3;jj++){
            memset(tab,0,sizeof(tab));
            blankParams.clear();
            veinParams.clear();
            vector<vector<int>> blankPos;
            vector<vector<int>> veinPos;
            string zero="0";
            if (ii>9) zero="";
            string plikStr=folder+zero+to_string(ii)+"_"+typ[jj]+".txt";
            string plikStr2=folder+zero+to_string(ii)+"_"+typ[jj]+".csv";
            ifstream plik(plikStr);
            int iter=0;
            while(!plik.eof()){
                plik>>x;
                plik>>y;
                if(plik.eof()) break;
                tab[x][y][ISTNIEJE]=1;
                plik>>tab[x][y][RED];
                plik>>tab[x][y][GREEN];
                plik>>tab[x][y][BLUE];
                plik>>tab[x][y][DECYZJA];
                plik>>tab[x][y][KCK];
                vector<int> a{x,y};
                if(tab[x][y][DECYZJA]==1) veinPos.push_back(a);
                else blankPos.push_back(a);
                iter++;
            }
            plik.close();
            //tutaj losuje które blank zostają wbrane (pierwsze tyle ile jest veinPos
            shuffle ( blankPos.begin(), blankPos.end(), std::mt19937(std::random_device()()));
            current.clear();
            ofstream plik2(plikStr2);

            plik2<<naglowek;
            for(int i=0;i<veinPos.size();i++){
                veinParams.push_back(generateParams(veinPos[i]));
                blankParams.push_back(generateParams(blankPos[i]));
                for(auto &j :veinParams[i]){
                    plik2<<j<<";";
                }

                plik2<<"1"<<endl;
                for(auto &j :blankParams[i]){
                    plik2<<j<<";";
                }
                plik2<<"0"<<endl;
            }
            plik2.close();
//            for (auto &i:veinParams){
//                for(auto &j :i){
//                    cout<<j<<" ";
//                }
//                cout<<endl;
//            }
            cout<<jj<<endl;
        }
        cout<<ii<<endl;
    }
    return 0;
}