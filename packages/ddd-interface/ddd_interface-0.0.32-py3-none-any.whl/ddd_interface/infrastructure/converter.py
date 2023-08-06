def entity_to_multi_entities(x, classes):
    return [clazz(**x._init_args) for clazz in classes]


    
def multi_entities_to_entity(clazz, classes):
    all_args = {}
    for args in [c._init_args for c in classes]:
        all_args.update(args)
    return clazz(**all_args)



class Converter:
    def to_entity(self, do):
        raise NotImplementedError


    def to_do(self, x):
        raise NotImplementedError


    def to_multi_entities(self, do, classes):
        return entity_to_multi_entities(self.to_entity(do), classes)