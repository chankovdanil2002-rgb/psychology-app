/**
 * Deferred — реализация отложенных объектов (аналог jQuery.Deferred).
 *
 * Жизненный цикл:
 *   pending  →  resolve()  →  'resolved'  →  done + always callbacks
 *   pending  →  reject()   →  'rejected'  →  fail + always callbacks
 *
 * API:
 *   .resolve(value)   — переводит deferred в состояние «выполнен»
 *   .reject(reason)   — переводит deferred в состояние «отклонён»
 *   .done(cb)         — cb вызывается при успехе (или сразу, если уже resolved)
 *   .fail(cb)         — cb вызывается при ошибке (или сразу, если уже rejected)
 *   .always(cb)       — cb вызывается в любом исходе
 *   .then(onOk, onErr)— цепочка, возвращает новый Deferred
 *   Deferred.when(…)  — ждёт ВСЕХ переданных Deferred; аналог $.when()
 */
class Deferred {
  constructor() {
    this.state = 'pending';  // 'pending' | 'resolved' | 'rejected'
    this._value = undefined;
    this._doneCallbacks   = [];
    this._failCallbacks   = [];
    this._alwaysCallbacks = [];

    // Внутренний Promise — чтобы можно было await deferred.promise
    this.promise = new Promise((res, rej) => {
      this._nativeResolve = res;
      this._nativeReject  = rej;
    });
    // Подавляем «unhandledRejection» если никто не вешал .fail()
    this.promise.catch(() => {});
  }

  // ── Управление состоянием ───────────────────────────────────────────────

  resolve(value) {
    if (this.state !== 'pending') return this;
    this.state  = 'resolved';
    this._value = value;
    this._nativeResolve(value);
    this._doneCallbacks.forEach(cb => cb(value));
    this._alwaysCallbacks.forEach(cb => cb(value));
    return this;
  }

  reject(reason) {
    if (this.state !== 'pending') return this;
    this.state  = 'rejected';
    this._value = reason;
    this._nativeReject(reason);
    this._failCallbacks.forEach(cb => cb(reason));
    this._alwaysCallbacks.forEach(cb => cb(reason));
    return this;
  }

  // ── Коллбэки ────────────────────────────────────────────────────────────

  /** Вызывается при успехе. Если уже resolved — выполняется немедленно. */
  done(callback) {
    if (this.state === 'resolved') callback(this._value);
    else this._doneCallbacks.push(callback);
    return this;  // цепочка
  }

  /** Вызывается при ошибке. Если уже rejected — выполняется немедленно. */
  fail(callback) {
    if (this.state === 'rejected') callback(this._value);
    else this._failCallbacks.push(callback);
    return this;  // цепочка
  }

  /** Вызывается в любом исходе. */
  always(callback) {
    if (this.state !== 'pending') callback(this._value);
    else this._alwaysCallbacks.push(callback);
    return this;  // цепочка
  }

  /**
   * Цепочка преобразований — аналог Promise.then().
   * Возвращает новый Deferred, что позволяет строить pipeline.
   */
  then(onFulfilled, onRejected) {
    const next = new Deferred();
    this.done(value => {
      try {
        next.resolve(onFulfilled ? onFulfilled(value) : value);
      } catch (e) {
        next.reject(e);
      }
    });
    this.fail(reason => {
      try {
        if (onRejected) next.reject(onRejected(reason));
        else next.reject(reason);
      } catch (e) {
        next.reject(e);
      }
    });
    return next;
  }

  // ── Статические методы ──────────────────────────────────────────────────

  /**
   * Deferred.when(...deferreds) — аналог $.when().
   *
   * Ждёт завершения ВСЕХ переданных Deferred.
   * - Если все resolved  → возвращаемый Deferred резолвится массивом результатов.
   * - Если хотя бы один rejected → возвращаемый Deferred отклоняется немедленно.
   */
  static when(...deferreds) {
    const combined = new Deferred();
    if (deferreds.length === 0) return combined.resolve([]);

    const results  = new Array(deferreds.length);
    let remaining  = deferreds.length;
    let rejected   = false;

    deferreds.forEach((d, index) => {
      d
        .done(value => {
          if (rejected) return;
          results[index] = value;
          remaining -= 1;
          if (remaining === 0) combined.resolve(results);
        })
        .fail(reason => {
          if (rejected) return;
          rejected = true;
          combined.reject(reason);
        });
    });

    return combined;
  }

  /**
   * Вспомогательный метод: оборачивает Promise или Axios-промис в Deferred.
   * Позволяет использовать Deferred API поверх любого асинхронного кода.
   */
  static fromPromise(promise) {
    const d = new Deferred();
    promise.then(value => d.resolve(value)).catch(err => d.reject(err));
    return d;
  }
}

export default Deferred;
