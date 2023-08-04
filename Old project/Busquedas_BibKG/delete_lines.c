#include <stdio.h>
#include <stdlib.h>
#define BUFFER_SIZE 1000
void deleteLine(FILE *src, FILE *temp, const int line);
void printFile(FILE *fptr);
int main(){
   FILE *src;
   FILE *temp;
   char ch;
   char path[100];
   int line;
   src=fopen("cprogramming.txt","w");
   printf("enter the text.press cntrl Z:
");
   while((ch = getchar())!=EOF){
      putc(ch,src);
   }
   fclose(src);
   printf("Enter file path: ");
   scanf("%s", path);
   printf("Enter line number to remove: ");
   scanf("%d", &line);
   src = fopen(path, "r");
   temp = fopen("delete.tmp", "w");
   if (src == NULL || temp == NULL){
      printf("Unable to open file.
");
      exit(EXIT_FAILURE);
   }
   printf("
File contents before removing line.

");
   printFile(src);
   // Move src file pointer to beginning
   rewind(src);
   // Delete given line from file.
   deleteLine(src, temp, line);
   /* Close all open files */
   fclose(src);
   fclose(temp);
   /* Delete src file and rename temp file as src */
   remove(path);
   rename("delete.tmp", path);
   printf("


File contents after removing %d line.

", line);
   // Open source file and print its contents
   src = fopen(path, "r");
   printFile(src);
   fclose(src);
   return 0;
}
void printFile(FILE *fptr){
   char ch;
   while((ch = fgetc(fptr)) != EOF)
   putchar(ch);
}
void deleteLine(FILE *src, FILE *temp, const int line){
   char buffer[BUFFER_SIZE];
   int count = 1;
   while ((fgets(buffer, BUFFER_SIZE, src)) != NULL){
      if (line != count)
         fputs(buffer, temp);
      count++;
   }
}