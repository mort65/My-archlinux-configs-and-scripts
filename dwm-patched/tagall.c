void
tagall(const Arg *arg) {
	if (!selmon->clients)
		return;
	/* if parameter starts with F, just move floating windows */
	Client* c;
	if(arg->ui & TAGMASK)
		for(c = selmon->clients; c; c = c->next) {
			if (TAGMASK == (c->tags | TAGMASK))
				c->tags = arg->ui & TAGMASK;
		}
	focus(NULL);
	arrange(selmon);
	updatecurrentdesktop();
}

void
tagallfloating(const Arg *arg) {
	if (!selmon->clients)
		return;
	/* if parameter starts with F, just move floating windows */
	Client* c;
	if(arg->ui & TAGMASK)
		for(c = selmon->clients; c; c = c->next) {
			if (c->isfloating && TAGMASK == (c->tags | TAGMASK))
				c->tags = arg->ui & TAGMASK;
		}
	focus(NULL);
	arrange(selmon);
	updatecurrentdesktop();
}
