def enforcedmethod(func):
    func.__enforcedmethod__ = True
    return func


class ABCMetaDict(type):

    def __call__(cls, *args, **kwargs):
        enforced = set()
        unenforced = set()

        # get two sets of attributes: enforced flag is set and enforced flag is not set
        for name, value in cls.__dict__.items():
            if getattr(value, "__enforcedmethod__", False):
                enforced.add(name)
            else:
                unenforced.add(name)

        for base in cls.__mro__:
            if base in [dict, object, cls]:
                # if the class is dict, object or this class, skip it
                # that way methods in those classes don't count as being imlemented
                continue

            for name, value in base.__dict__.items():
                # if the item is flagged as enforced and isn't already in the
                # unenforced set (i.e., there's an implementation somewhere)
                # then added to the enforced set
                if getattr(value, "__enforcedmethod__", False):
                    if name not in unenforced:
                        enforced.add(name)
                else:
                    # this item isn't flagged as enforced, so add it to the unenforced list
                    unenforced.add(name)
                    if name in enforced:
                        # if the item was previously flagged as enforced, we can now remove it
                        # since we've found an implementation
                        enforced.remove(name)
        if enforced:
            raise TypeError("Can't instantiate abstract class {} "
                            "with enforced methods {}".format(
                                cls.__name__, ', '.join(enforced)))
        else:
            return super(ABCMetaDict, cls).__call__(*args, **kwargs)
