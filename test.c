int c;

int avg(int count, int *value) {
  int i;
  int total;
  total = 0;
  for (i = 0; i < count; i++) {
    total = total + value[i];
  }
  return (total / count);
}

// comment

int main(int test) {
  int studentNumber, count, i, sum;
  int mark[4];
  float average;
  int cc[5];
  printf("%s", cc);
  studentNumber = 0;
  count = 4;
  sum = 0;
  if(0 == 0);
  for (i = 0; i < count; i++) {
    --studentNumber;
    mark[i] = i * 30;
    sum = sum + mark[i];
    average = avg(i + 1, mark);
    if (average > 40) {
      printf("%f", average);
    }
  }
}
