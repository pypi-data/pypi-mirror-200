def entity_to_multi_entities(x, classes):
    return [clazz(**x._init_args) for clazz in classes]


    
def multi_entities_to_entity(clazz, classes):
    all_args = {}
    for args in [c._init_args for c in classes]:
        all_args.update(args)
    return clazz(**all_args)



class Assembler:
    def to_entity(self, dto):
        raise NotImplementedError
    

    def to_dto(self, x):
        raise NotImplementedError
    

    def to_multi_entities(self, dto, classes):
        return entity_to_multi_entities(self.to_entity(dto), classes)

