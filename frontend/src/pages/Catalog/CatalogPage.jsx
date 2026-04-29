import { useCallback, useEffect, useRef, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getPsychologists, getSpecializations } from '../../api';
import Pagination from '../../components/ui/Pagination';
import StarRating from '../../components/ui/StarRating';
import { extractData, extractList, formatPrice, truncateText, getCookie, setCookie } from '../../utils/helpers';
import Deferred from '../../utils/deferred';
import styles from './CatalogPage.module.css';

export default function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [psychologists, setPsychologists] = useState([]);
  const [specializations, setSpecializations] = useState([]);
  const [initialLoading, setInitialLoading] = useState(true);
  const [loading, setLoading]               = useState(false);
  const [totalPages, setTotalPages]         = useState(1);
  const [filtersOpen, setFiltersOpen]       = useState(false);
  const [loadError, setLoadError]           = useState(null);

  const currentPage = parseInt(searchParams.get('page') || '1', 10);
  const search      = searchParams.get('search') || '';
  const ordering    = searchParams.get('ordering') || getCookie('catalog_ordering') || '-average_rating';
  const specFilter  = searchParams.get('specialization') || '';

  const searchRef     = useRef(null);
  const debounceRef   = useRef(null);
  const initialDone   = useRef(false);

  // ── Начальная загрузка: специализации + психологи одновременно ──────────
  // Демонстрирует Deferred.when() — ждём ОБА запроса параллельно.
  useEffect(() => {
    const dSpecs  = Deferred.fromPromise(getSpecializations());
    const dPsychs = Deferred.fromPromise(
      getPsychologists({ page: 1, ordering })
    );

    // $.when() — продолжаем только когда оба запроса завершены
    Deferred.when(dSpecs, dPsychs)
      .done(([specsRes, psychsRes]) => {
        // .done() — вызывается только при полном успехе обоих запросов
        setSpecializations(extractList(specsRes));

        const d = extractData(psychsRes);
        if (d?.results) {
          setPsychologists(d.results);
          setTotalPages(Math.ceil((d.count || 0) / 12));
        } else {
          setPsychologists(Array.isArray(d) ? d : []);
          setTotalPages(1);
        }
        setLoadError(null);
        initialDone.current = true;
      })
      .fail(err => {
        // .fail() — вызывается если хотя бы один из запросов упал
        console.error('[Catalog] Ошибка начальной загрузки:', err);
        setLoadError('Не удалось загрузить данные. Попробуйте обновить страницу.');
        setPsychologists([]);
      })
      .always(() => {
        // .always() — выполняется в любом случае (убираем прелоадер)
        setInitialLoading(false);
      });
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Перезагрузка при изменении фильтров (после первого рендера) ─────────
  // Демонстрирует одиночный Deferred с .then() / .fail() / .always()
  useEffect(() => {
    if (!initialDone.current) return;

    const params = { page: currentPage, ordering };
    if (search)     params.search          = search;
    if (specFilter) params.specialization  = specFilter;

    setLoading(true);
    setLoadError(null);

    // Оборачиваем Axios-промис в Deferred
    const dPsychs = Deferred.fromPromise(getPsychologists(params));

    dPsychs
      // .then() — трансформируем ответ в нужный формат
      .then(res => {
        const d = extractData(res);
        return d?.results
          ? { list: d.results, pages: Math.ceil((d.count || 0) / 12) }
          : { list: Array.isArray(d) ? d : [], pages: 1 };
      })
      // .done() на результат .then()
      .done(({ list, pages }) => {
        setPsychologists(list);
        setTotalPages(pages);
      })
      .fail(err => {
        console.error('[Catalog] Ошибка при обновлении списка:', err);
        setLoadError('Не удалось обновить список психологов.');
        setPsychologists([]);
      })
      .always(() => setLoading(false));
  }, [currentPage, search, ordering, specFilter]);

  const updateParam = useCallback(
    (key, value) => {
      const params = new URLSearchParams(searchParams);
      if (value) params.set(key, value);
      else params.delete(key);
      if (key !== 'page') params.set('page', '1');
      setSearchParams(params);
    },
    [searchParams, setSearchParams]
  );

  const handleSearchInput = (e) => {
    const val = e.target.value;
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => updateParam('search', val), 300);
  };

  // ── Прелоадер начальной загрузки ────────────────────────────────────────
  if (initialLoading) {
    return (
      <div className={styles.preloaderWrap}>
        <div className={styles.spinner} />
        <p className={styles.preloaderText}>Загружаем психологов...</p>
      </div>
    );
  }

  return (
    <div className={styles.catalog}>
      <h1 className={styles.title}>Каталог психологов</h1>

      {/* Верхняя панель */}
      <div className={styles.topBar}>
        <input
          ref={searchRef}
          className={styles.searchInput}
          type="text"
          placeholder="Поиск по имени..."
          defaultValue={search}
          onChange={handleSearchInput}
        />
        <select
          className={styles.sortSelect}
          value={ordering}
          onChange={(e) => {
            setCookie('catalog_ordering', e.target.value);
            updateParam('ordering', e.target.value);
          }}
        >
          <option value="-average_rating">По рейтингу</option>
          <option value="price">Цена: по возрастанию</option>
          <option value="-price">Цена: по убыванию</option>
          <option value="-experience_years">По опыту</option>
        </select>
        <button
          className={styles.filterToggle}
          onClick={() => setFiltersOpen(!filtersOpen)}
        >
          Фильтры {filtersOpen ? '▲' : '▼'}
        </button>
      </div>

      <div className={styles.content}>
        {/* Боковая панель */}
        <aside className={`${styles.sidebar} ${filtersOpen ? styles.sidebarOpen : ''}`}>
          <h3>Специализации</h3>
          <div className={styles.filterList}>
            <label className={styles.filterItem}>
              <input
                type="radio"
                name="spec"
                checked={!specFilter}
                onChange={() => updateParam('specialization', '')}
              />
              Все
            </label>
            {specializations.map((s) => (
              <label key={s.id} className={styles.filterItem}>
                <input
                  type="radio"
                  name="spec"
                  checked={specFilter === s.slug}
                  onChange={() => updateParam('specialization', s.slug)}
                />
                {s.name}
              </label>
            ))}
          </div>
        </aside>

        {/* Карточки */}
        <main className={styles.main}>
          {loadError && (
            <p className={styles.error}>{loadError}</p>
          )}

          {loading ? (
            <div className={styles.loadingOverlay}>
              <div className={styles.spinnerSm} />
            </div>
          ) : psychologists.length === 0 && !loadError ? (
            <p className={styles.empty}>Психологи не найдены</p>
          ) : (
            <>
              <div className={styles.grid}>
                {psychologists.map((p) => (
                  <Link to={`/psychologists/${p.id}`} key={p.id} className={styles.card}>
                    <div className={styles.cardPhoto}>
                      {p.photo ? (
                        <img src={p.photo} alt={p.full_name} />
                      ) : (
                        <div className={styles.photoPlaceholder}>
                          {(p.full_name || '?')[0]}
                        </div>
                      )}
                    </div>
                    <div className={styles.cardBody}>
                      <h3 className={styles.cardName}>{p.full_name}</h3>
                      {p.specializations && (
                        <p className={styles.cardSpecs}>
                          {(Array.isArray(p.specializations) ? p.specializations : []).join(', ')}
                        </p>
                      )}
                      <div className={styles.cardRating}>
                        <StarRating value={p.average_rating || 0} size="sm" showValue />
                        <span className={styles.reviewCount}>({p.total_reviews || 0})</span>
                      </div>
                      {p.bio && <p className={styles.cardBio}>{truncateText(p.bio, 100)}</p>}
                      <div className={styles.cardFooter}>
                        {p.experience_years != null && (
                          <span>Опыт: {p.experience_years} лет</span>
                        )}
                        <span className={styles.cardPrice}>{formatPrice(p.price)}</span>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={(p) => updateParam('page', String(p))}
              />
            </>
          )}
        </main>
      </div>
    </div>
  );
}
