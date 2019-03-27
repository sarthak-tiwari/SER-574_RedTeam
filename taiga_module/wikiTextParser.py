from taiga_module import taigaWiki


def wikiTextParser(projectSlug,wikiSlug):
    wikiContent = taigaWiki.getWiki(projectSlug, wikiSlug)
    input_dict = wikiContent.split("\n")
    input_dict.append(':')

    currentMOM = {}
    MOM = {}

    counter = 0
    currentKey = ''

    for i in range(len(input_dict)):
        raw_data = input_dict[i]
        data = raw_data[3:-4]
        if '=' in data:
            if len(currentMOM) == 0:
                continue
            else:
                counter = counter + 1
                MOM.update({'MoM-' + str(counter): currentMOM})
                currentMOM = {}
        else:
            if ':' in data:
                currentKey = data.split(':')[0].strip()
                if ':' in input_dict[i+1]:
                    currentValue = data.split(':')[1].strip()
                    currentMOM.update({currentKey: currentValue})
                else:
                    currentList = []
                    while ':' not in input_dict[i+1]:
                        raw_data = input_dict[i+1]
                        data = raw_data[3:-4]
                        currentList.append(data)
                        if ':' not in input_dict[i + 1]:
                            i = i + 1
                        else:
                            break

                    currentMOM.update({currentKey: currentList})
                    currentList = []

    ### parsing ends
    return MOM

wikiTextParser("cram1206-test","samplewiki")