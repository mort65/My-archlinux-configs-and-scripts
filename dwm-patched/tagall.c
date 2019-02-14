void
tagall(const Arg *arg) {
	if (!selmon->clients)
		return;
	if(arg->ui & TAGMASK) {
		Client* c;
		for(c = selmon->clients; c; c = c->next) {
			if (ISVISIBLE(c) && TAGMASK == (c->tags | TAGMASK))
				c->tags = arg->ui & TAGMASK;
		}
	}
	focus(NULL);
	arrange(selmon);
	updatecurrentdesktop();
}

void
tagallfloating(const Arg *arg) {
	if (!selmon->clients)
		return;
	if(arg->ui & TAGMASK) {
		Client* c;
		for(c = selmon->clients; c; c = c->next) {
			if (c->isfloating && ISVISIBLE(c) && TAGMASK == (c->tags | TAGMASK))
				c->tags = arg->ui & TAGMASK;
		}
	}
	focus(NULL);
	arrange(selmon);
	updatecurrentdesktop();
}
