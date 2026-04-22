import { useState, useRef } from 'react';
import styles from './FileUpload.module.css';

/**
 * Компонент загрузки файла с превью для изображений и PDF.
 */
export default function FileUpload({
  label,
  name,
  accept = 'image/*,.pdf',
  error,
  onChange,
  currentFile,
  className = '',
}) {
  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState('');
  const inputRef = useRef(null);

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);

    // Генерируем превью для изображений
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (ev) => setPreview(ev.target.result);
      reader.readAsDataURL(file);
    } else {
      // Для не-изображений (PDF) показываем только имя файла
      setPreview(null);
    }

    if (onChange) {
      onChange(file);
    }
  };

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleRemove = () => {
    setPreview(null);
    setFileName('');
    if (inputRef.current) inputRef.current.value = '';
    if (onChange) onChange(null);
  };

  const hasFile = preview || fileName;
  // currentFile — это строка URL для уже загруженных файлов
  const existingPreview = currentFile && typeof currentFile === 'string';

  return (
    <div className={`${styles.wrapper} ${className}`}>
      {label && <label className={styles.label}>{label}</label>}

      <input
        ref={inputRef}
        type="file"
        name={name}
        accept={accept}
        onChange={handleChange}
        className={styles.hiddenInput}
      />

      {/* Область превью */}
      {(preview || existingPreview) && (
        <div className={styles.previewArea}>
          <img
            src={preview || currentFile}
            alt="Превью"
            className={styles.previewImage}
          />
        </div>
      )}

      {fileName && !preview && (
        <div className={styles.fileName}>{fileName}</div>
      )}

      <div className={styles.actions}>
        <button type="button" className={styles.uploadBtn} onClick={handleClick}>
          {hasFile || existingPreview ? 'Изменить файл' : 'Выбрать файл'}
        </button>
        {hasFile && (
          <button type="button" className={styles.removeBtn} onClick={handleRemove}>
            Удалить
          </button>
        )}
      </div>

      {error && (
        <span className={styles.error} role="alert">
          {error}
        </span>
      )}
    </div>
  );
}
