/*
	Version 1.0
	Card class used as the foundation for other cards
*/

#ifndef BASECARD_H_
#define BASECARD_H_

#include <string>

using namespace std;

class BaseCard {
public:
	//BaseCard();



private:
	int hp = 1, 
		dmg = 0;
	string title = "Base Card", 
		descriptor = "This is a base card.";
};

#endif