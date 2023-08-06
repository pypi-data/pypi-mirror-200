![](https://www.semantha.de/wp-content/uploads/semantha-inverted.svg)

# semantha® SDK

The semantha SDK is a high-level REST client to access the [semantha](http://semantha.ai) API.
The SDK is still under development.
An overview of the current progress (i.e. implemented and tested resources and endpoints) may be found at the end of
this document (State of Development).
The semantha SDK is compatible with python >= 3.8.

### Disclaimer

**IMPORTANT:** The SDK is under development and interfaces may change at any time without notice.
Use with caution and on own risk.

### Update Note

Version 4.5.0 comes with a major restructuring of the SDK.
All sub-resources are directly accessible (instead of invoking getters).
That also means that (except for a few) all functions are plain get/post/delete/put/patch.
For example, in Versions < 4.5.0 a domain resource was fetched using `semantha_sdk.domains.get_one("domain_name")`.
Starting with 4.5.0 it is `semantha_sdk.domains("domain_name")`.
That also means that get/post/put/patch functions return semantha model objects (and never resources), which makes usage more consistent.

### Access

To access semantha's API you will need an API and a server url.
Both can be requested via [this contact form](https://www.semantha.de/request/).

### Basic Usage

#### Import

```
import semantha_sdk
```

#### Authentication

```
semantha = semantha_sdk.login(url="<semantha platform server URL>", key="<your key>")
# or
semantha = semantha_sdk.login(url="<semantha platform server URL>", key_file="<path to your key file (json format)>")
```

#### End-point (Resource) Access

```
# end-points (resp. resources) can be used like objects
current_user = semantha.currentuser
my_domain = semantha.domains("my_domain")

# they may have sub-resources, which can be retrieved as objects as well
reference_documents = my_domain.referencedocuments
```

#### CRUD on End-points

```
# CRUD operations are functions
domain_settings = my_domain.settings.get()
my_domain.referencedocuments.delete() (deletes ALL reference document/library entries)
```

#### Function Return Types & semantha Data Model

```
# some functions only return None, e.g.
my_domain.referencedocuments.delete() # returns NoneType

# others return built in types, e.g
roles_list = currentuser.roles.get() # returns list[str]

# but most return objects of the semantha Data Model
# (all returned objects are instances of frozen dataclasses)
settings = my_domain.settings.get() # returns instance of DomainSettings
# attributes can be accessed as properties, e.g.
settings.enable_tagging # returns true or false
# Data Model objects may be complex
document = my_domain.references.post(file=a, referencedocument=b) # returns instance of Document
# the following returns the similarity value of the first references of the first sentence of the
# the first paragraph on the first page of the document (if a reference was found for this sentence)
similarity = pages[0].contents[0].paragraphs[0].references[0].similarity # returns float
```

### State of Development

The following resources and end-points are fully functional and (partially) tested:

- [X] login -> API
    - [X] .currentuser -> CurrentUser
        - [X] get -> UserData(SemanthaModelEntity)
        - [X] roles -> CurrentUserRoles
          - [x] get -> list[str]
    - [X] .diff -> Diff
        - [X] post -> list[Diff(SemanthaModelEntity)]
    - [X] .info -> VersionInfo
        - [X] get -> VersionInfo
    - [x] .languages -> list[str]
    - [X] .domains -> Domains
        - [X] get -> list[Domain(SemanthaModelEntity)]
    - [X] .domains("domain_name") -> Domain
        - [X] .documentannotations -> DocumentAnnotations
            - [ ] post -> not yet implemented
        - [X] .documentclasses -> DocumentClasses
            - [X] get -> list[DocumentClass(SemanthaModelEntity)]
            - [X] post -> DocumentClass(SemanthaModelEntity)
            - [X] delete -> None
        - [X] .documentclasses("id") -> DocumentClass
            - [X] get -> DocumentClass(SemanthaModelEntity)
            - [X] delete -> None
            - [X] put -> DocumentClass(SemanthaModelEntity)
            - [x] documentclasses -> InnerDocumentClasses
                - [x] get -> list[DocumentClass(SemanthaModelEntity)]
                - [x] post -> DocumentClass(SemanthaModelEntity)
            - [x] referencedocuments -> InnerReferenceDocuments
                - [x] get -> list[Document(SemanthaModelEntity)]
                - [x] patch -> None
                - [x] delete -> None
        - [X] .documentcomparisons -> DocumentComparisons
            - [ ] post -> not yet implemented
          - [X] .documents -> Documents
              - [X] post -> list[Document(SemanthaModelEntity)]
        - [x] .modelinstances -> ModelInstance
        - [x] .modelclasses -> ModelClass
        - [X] .referencedocuments -> ReferenceDocuments
            - [X] get -> ReferenceDocuments(SemanthaModelEntity)
            - [X] delete -> None
            - [X] post -> list[DocumentInformation(SemanthaModelEntity)]
            - [x] .clusters -> DocumentCluster
              - [x] get -> DocumentCluster(SemanthaModelEntity)
            - [x] .statistic -> Statistics
              - [x] get -> Statistic(SemanthaModelEntity)
            - [x] .namedentities -> NamedEntities
              - [x] get -> Optional[NamedEntities(SemanthaModelEntity)]
        - [x] .referencedocuments("id") -> ReferenceDocument
            - [X] get -> Document(SemanthaModelEntity)
            - [X] delete -> None
            - [X] patch -> DocumentInformation(SemanthaModelEntity)
            - [X] .paragraphs("id") -> ReferenceDocumentParagraph
                - [X] get -> Paragraph(SemanthaModelEntity)
                - [X] patch -> Paragraph(SemanthaModelEntity)
                - [X] delete -> None
            - [X] .sentences("id") -> ReferenceDocumentSentence
                - [x] get -> Sentence(SemanthaModelEntity)
        - [X] .references -> References
            - [X] post -> Document(SemanthaModelEntity)
        - [x] .settings -> DomainSettings
            - [X] get -> DomainSettings(SemanthaModelEntity)
            - [X] patch -> DomainSettings(SemanthaModelEntity)
        - [x] .similaritymatrix -> List[MatrixRow]
            - [x] .clusters -> List[MatrixRow]
        - [ ] .tags -> DomainTags
            - [X] get -> list[str]
            - .("tag").referencedocuments
              - [x] get
              - [x] delete
        - [x] .validation -> SemanticModel
    - [ ] .model
      - [x] .domains("domain_name")
        - [x] .boostwords -> Boostwords
            - [x] get -> list[Boostword(SemanthaModelEntity)]
            - [X] delete -> None
            - [X] post_word -> Boostword(SemanthaModelEntity)
            - [X] post_regex -> Boostword(SemanthaModelEntity)
        - [x] .boostwords("id") -> Boostword
            - [X] get -> Boostword(SemanthaModelEntity)
            - [X] delete -> None
            - [X] put_word -> Boostword(SemanthaModelEntity)
            - [X] put_regex -> Boostword(SemanthaModelEntity)
        - [x] .synonyms -> Synonyms
            - [X] get -> list[Synonym(SemanthaModelEntity)]
            - [X] delete -> None
            - [X] post_word -> Synonym(SemanthaModelEntity)
            - [X] post_regex -> Synonym(SemanthaModelEntity)
        - [x] .synonyms("id") -> Synonym
            - [X] get -> Synonym(SemanthaModelEntity)
            - [X] delete -> None
            - [X] put_word -> Synonym(SemanthaModelEntity)
            - [X] put_regex -> Synonym(SemanthaModelEntity)
        - [x] .datatypes -> list[str]