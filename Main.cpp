#include <SFML/Graphics.hpp>
#include <SFML/Audio.hpp>

// Structure used for screen size selection
struct ScreenRes {
    int x, y;
} defRes {1280, 720}, normRes = {1980, 1080};



int main()
{
    int winWidth = defRes.x;
    int winHeight  = defRes.y;
    sf::RenderWindow window(sf::VideoMode(winWidth, winHeight), "PaperCut");

    // Play music
    /*
    sf::Music mainSong;
    if(!music.openfromFile(--NAMEOFFILE--)) return EXIT_FAILURE;
    mainSong.play();
    */

    sf::Texture playerTexture = sf::Texture();
    playerTexture.loadFromFile("images\playercard.png");

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        window.display();
    }

    return 0;
}