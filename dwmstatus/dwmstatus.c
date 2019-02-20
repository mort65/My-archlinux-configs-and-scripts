/*
 * Copy me if you can.
 * by 20h
 */

#define _BSD_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <strings.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <X11/Xlib.h>

long cpu_work = 0, cpu_total = 0;

static Display *dpy;

char *
smprintf(char *fmt, ...)
{
	va_list fmtargs;
	char *ret;
	int len;

	va_start(fmtargs, fmt);
	len = vsnprintf(NULL, 0, fmt, fmtargs);
	va_end(fmtargs);

	ret = malloc(++len);
	if (ret == NULL) {
		perror("malloc");
		exit(1);
	}

	va_start(fmtargs, fmt);
	vsnprintf(ret, len, fmt, fmtargs);
	va_end(fmtargs);

	return ret;
}

char*
runcmd(char* cmd) {
	FILE* fp = popen(cmd, "r");
	if (fp == NULL) return NULL;
	char ln[20];
	fgets(ln, sizeof(ln)-1, fp);
	pclose(fp);
	ln[strlen(ln)-1]='\0';
	return smprintf("%s", ln);
}

char *
getdatetime(void)
{
	char datetime[17];
	sscanf(runcmd("date '+%a %d %b %H:%M'"), "%[^\n]%*c", datetime);
	return smprintf("%s", datetime);
}

void
setstatus(char *str)
{
	XStoreName(dpy, DefaultRootWindow(dpy), str);
	XSync(dpy, False);
}

char *
readfile(char *base, char *file)
{
	char *path, line[513];
	FILE *fd;

	memset(line, 0, sizeof(line));

	path = smprintf("%s/%s", base, file);
	fd = fopen(path, "r");
	free(path);
	if (fd == NULL)
		return NULL;

	if (fgets(line, sizeof(line)-1, fd) == NULL)
		return NULL;
	fclose(fd);

	return smprintf("%s", line);
}

char *
getcpu(void) {
    FILE *fd;
    long jif1, jif2, jif3, jif4, jif5, jif6, jif7;
    long work, total;
    int load;

    fd = fopen("/proc/stat", "r");
    fscanf(fd, "cpu %ld %ld %ld %ld %ld %ld %ld", &jif1, &jif2, &jif3, &jif4, &jif5, &jif6, &jif7);
    work = jif1 + jif2 + jif3 + jif6 + jif7;
    total = work + jif4 + jif5;

    fclose(fd);

    load = 100 * (work - cpu_work) / (total - cpu_total);

    cpu_work = work;
    cpu_total = total;

    return smprintf("%d%%", load);
}

char *
gettemperature(char *base, char *sensor)
{
	char *co;

	co = readfile(base, sensor);
	if (co == NULL)
		return smprintf("");
	return smprintf("%02.0f°C", atof(co) / 1000);
}

char *
getmem(void) {
    FILE *fd;
    long total, free, shared, buffer, cached, srec, totalused, totalcached;
    int result, ch, line, newlines = 0;
    fd = fopen("/proc/meminfo", "r");
    fscanf(fd, "MemTotal: %ld kB\n", &total);
    fscanf(fd, "MemFree: %ld kB\n", &free);
    line = 2;
    while ((ch = getc(fd)) != EOF) {
	    if (ch == '\n') {
		    if (++newlines == line - 1) {
			    newlines = 0;
			    break;
		    }
	    }
    }
    fscanf(fd, "Buffers: %ld kB\n", &buffer);
    fscanf(fd, "Cached: %ld kB\n", &cached);
    line = 16;
    while ((ch = getc(fd)) != EOF) {
	    if (ch == '\n') {
		    if (++newlines == line - 1) {
			    newlines = 0;
			    break;
		    }
	    }
    }
    fscanf(fd, "Shmem: %ld kB\n", &shared);
    line=3;
    while ((ch = getc(fd)) != EOF) {
	    if (ch == '\n') {
		    if (++newlines == line - 1) {
			    break;
		    }
	    }
    }
    fscanf(fd, "SReclaimable: %ld kB\n", &srec);
    fclose(fd);
    totalcached = ((cached + srec) - shared);
    totalused = total - free;
    result = 100 * (totalused - (buffer + totalcached)) / total;
    return smprintf("%d%%", result);
}

int
main(void)
{
	char *status;
	char *mem;
	char *cpu;
	char *time;
	char *tc, *tg;
	char clr[50] = {'\0'};

	if (!(dpy = XOpenDisplay(NULL))) {
		fprintf(stderr, "dwmstatus: cannot open display.\n");
		return 1;
	}

	for (;;sleep(2)) {
		mem = getmem();
		cpu = getcpu();
		time = getdatetime();
		tc = gettemperature("/sys/devices/platform/coretemp.0/hwmon/hwmon1", "temp1_input");
		tg = gettemperature("/sys/devices/pci0000:00/0000:00:01.0/0000:01:00.0/hwmon/hwmon0", "temp1_input");
		status = smprintf("C[%s %s] G[%s] R[%s] T[%s]",
				cpu, tc, tg, mem, time);
		setstatus(clr);
		setstatus(status);

		free(tc);
		free(tg);
		free(mem);
		free(cpu);
		free(time);
		free(status);
	}

	XCloseDisplay(dpy);

	return 0;
}

