# gallica-getter

Find documents where a word occurs, context for the occurrence, full text for OCR document pages. Compose Gallica services using Python classes that represent each service.

## Examples

Here are a few examples from a JSON API I am currently hosting:

```python
async def get_documents_with_occurrences(
    args: ContextSearchArgs,
    on_get_total_records: Callable[[int], None],
    on_get_origin_urls: Callable[[List[str]], None],
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
) -> List[VolumeRecord]:
    """Queries Gallica's SRU API to get metadata for a given term in the archive."""

    link = None
    if args.link_distance and args.link_term:
        link = (args.link_term, args.link_distance)

    # get the volumes in which the term appears
    volume_Gallica_wrapper = VolumeOccurrence()
    gallica_records = await volume_Gallica_wrapper.get(
        terms=args.terms,
        start_date=make_date_from_year_mon_day(args.year, args.month, args.day),
        end_date=make_date_from_year_mon_day(args.end_year, args.end_month, args.day),
        codes=args.codes,
        source=args.source,
        link=link,
        limit=args.limit,
        start_index=args.cursor or 0,
        sort=args.sort,
        on_get_total_records=on_get_total_records,
        on_get_origin_urls=on_get_origin_urls,
        session=session,
        semaphore=semaphore,
    )

    return list(gallica_records)

```

```python
async def get_sample_context_in_documents(
    records: List[VolumeRecord],
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
) -> List[ExtractRoot]:
    """Queries Gallica's search result API to show a sample of context instead of the entire batch."""

    # warn if terms length is greater than 1
    if any(len(record.terms) > 1 for record in records):
        print(
            "Warning: using sample context for multi-word terms; only the first term will be used."
        )
    context_snippet_wrapper = ContextSnippets()
    context = await context_snippet_wrapper.get(
        [(record.ark, record.terms[0]) for record in records],
        session=session,
        semaphore=semaphore,
    )
    return list(context)
```

```python
async def get_context_include_full_page(
    keyed_docs: Dict[str, VolumeRecord],
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    context_source: Callable,
):
    """Queries Context and PageText to get the text of each page a term occurs on."""
    page_text_wrapper = PageText()
    queries: List[PageQuery] = []

    # build records to be filled with page text for each page w/occurrence
    gallica_records: Dict[str, GallicaRecordFullPageText] = {
        record.ark: GallicaRecordFullPageText(**record.dict(), context=[])
        for record in keyed_docs.values()
    }

    for context_response in await context_source(
        records=list(keyed_docs.values()), session=session, semaphore=sem
    ):
        record = keyed_docs[context_response.ark]
        for page in context_response.pages:
            queries.append(
                PageQuery(
                    ark=record.ark,
                    page_num=int(page.page_num),
                )
            )
    page_data = await page_text_wrapper.get(
        page_queries=queries, semaphore=sem, session=session
    )
    for occurrence_page in page_data:
        record = gallica_records[occurrence_page.ark]
        terms_string = " ".join(record.terms)

        record.context.append(
            {
                "page_num": occurrence_page.page_num,
                "text": occurrence_page.text,
                "page_url": f"{record.url}/f{occurrence_page.page_num}.image.r={terms_string}",
            }
        )
    return list(gallica_records.values())
```





