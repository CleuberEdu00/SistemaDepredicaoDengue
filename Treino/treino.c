#include <stdio.h>

int main(){
    char nome[20];

    printf("Digite o nome: ");
    for(int i = 0; i < 20; i++){
        scanf("%s", &nome[i]);
    }

     for(int j = 0; j < 20; j++){
        printf("%s", nome[j]);
    }

    return 0;
}
