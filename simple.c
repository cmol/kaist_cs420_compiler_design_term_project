int glob;

void lal(int c) {
  printf("%d", glob);
}

void main(void) {
  int c;
  c = 1;
  glob = 4;
  if(c == 1) {
    lal(c);
  }
}
