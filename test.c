int c;

int avg(int count, int value) {
  int i;
  int total;
  int sum;
  sum = 0;
  for (i = 1; i < count; i = i + 1) {
    total = total + value[i];
  }
  return (total / count);
}

int main(void) {
  int studentNumber, count, i, sum;
  int mark[4];
  int average;
  count = 4;
  sum = 0;
  if(0 == 0);
  for (i = 0; i < count; i = i + 1) {
    mark[i] = i * 30;
    sum = sum + mark[i];
    average = avg(i + 1, mark);
    if (average > 40) {
      printf("%f", average);
    }
  }
}
