#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define INPUT_BUF argv[1]

int main(int argc, char *argv[]){
    int mask[26]; 
    if (argc == 3){
        int window_size = atoi(argv[2]);
        char *window = (char*)calloc(window_size , sizeof(char));
        size_t input_size = strlen(INPUT_BUF);
        for (int x = 0; x < input_size; ++x){
            if (x >= 4){
                for (int i = 0; i<26; i++){
                    mask[i] = 0;
                }
                int cont = 1;
                for (int y = 0; y < window_size; ++y){
                    if (mask[window[y] - 97]){
                        cont = 0;
                    }
                    mask[window[y]-97] = 1;
                    }
                if (cont){
                    printf("\n ANSWER IS %d\n", x);
                    free(window);
                    return 0;
                }
                }
            
            window[x%window_size] = INPUT_BUF[x];
            }

        free(window);
    }
    else{
        printf("Expected input of form <string input> <int window_size>");
    }
    return 1;
}
